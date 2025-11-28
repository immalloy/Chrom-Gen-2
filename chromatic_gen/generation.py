"""Core audio generation utilities for chromatic scale creation."""
from __future__ import annotations

from pathlib import Path
from typing import List

import parselmouth

DEFAULT_SAMPLE_RATE = 48000


class SampleSetEmptyError(RuntimeError):
    """Raised when no numbered samples are found in the provided directory."""


def _create_gap(gap_seconds: float) -> parselmouth.Sound:
    return parselmouth.praat.call(
        "Create Sound from formula", "Gap", 1, 0, float(gap_seconds), DEFAULT_SAMPLE_RATE, "0"
    )


def _load_samples(sample_dir: Path) -> List[parselmouth.Sound]:
    samples: List[parselmouth.Sound] = []
    sample_index = 1

    while (sample_dir / f"{sample_index}.wav").exists():
        loaded_sound = parselmouth.Sound(str(sample_dir / f"{sample_index}.wav"))
        resampled = parselmouth.praat.call(loaded_sound, "Resample", DEFAULT_SAMPLE_RATE, 1)
        samples.append(parselmouth.praat.call(resampled, "Convert to mono"))
        sample_index += 1

    if not samples:
        raise SampleSetEmptyError("No numbered .wav samples found in the selected folder.")

    return samples


def _pitch_sample(
    sample: parselmouth.Sound, semitone_offset: int, base_note: int, base_octave: int
) -> parselmouth.Sound:
    manipulation = parselmouth.praat.call(sample, "To Manipulation", 0.05, 60, 600)
    pitch_tier = parselmouth.praat.call(manipulation, "Extract pitch tier")

    midi_note = base_note + 12 * base_octave + semitone_offset

    parselmouth.praat.call(
        pitch_tier,
        "Formula",
        f"16.3516 * (2 ^ ({midi_note}/12))",
    )
    parselmouth.praat.call([pitch_tier, manipulation], "Replace pitch tier")

    return parselmouth.praat.call(manipulation, "Get resynthesis (overlap-add)")


def _ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def generate_chromatic_scale(
    sample_path: Path,
    semitones: int,
    gap_seconds: float,
    starting_note_index: int,
    starting_octave: int,
    pitched: bool,
    dump_samples: bool,
) -> Path:
    """
    Generate a chromatic scale from numbered samples in ``sample_path``.

    The directory is expected to contain files named ``1.wav``, ``2.wav``, etc.
    A resulting ``chromatic.wav`` is written to ``sample_path`` and the
    ``pitched_samples`` directory is populated when requested.
    """

    samples = _load_samples(sample_path)
    gap_sound = _create_gap(gap_seconds)

    pitched_sounds: List[parselmouth.Sound] = []
    spaced_sounds: List[parselmouth.Sound] = []

    for offset in range(semitones):
        base_sample = samples[offset % len(samples)]
        if pitched:
            pitched_sound = _pitch_sample(
                base_sample, offset, starting_note_index, starting_octave
            )
        else:
            pitched_sound = base_sample

        pitched_sounds.append(pitched_sound)
        spaced_sounds.extend([pitched_sound, gap_sound])

    chromatic = parselmouth.Sound.concatenate(spaced_sounds)

    chromatic_path = sample_path / "chromatic.wav"
    chromatic.save(str(chromatic_path), "WAV")

    if dump_samples and pitched:
        output_dir = sample_path / "pitched_samples"
        _ensure_directory(output_dir)
        for index, pitched_sound in enumerate(pitched_sounds, start=1):
            pitched_sound.save(str(output_dir / f"pitched_{index}.wav"), "WAV")

    return chromatic_path
