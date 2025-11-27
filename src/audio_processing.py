from typing import Tuple
import numpy as np
import parselmouth

SR = 48_000
C0_HZ = 16.3516
TIME_STEP_S = 0.01
FADE_MS = 8.0
PEAK_TARGET = 0.95

def load_mono(path: str) -> parselmouth.Sound:
    snd = parselmouth.Sound(path)
    snd = parselmouth.praat.call(snd, "Resample", SR, 1)
    snd = parselmouth.praat.call(snd, "Convert to mono")
    return snd

def hz_from_c0(semitone_from_c0: int) -> float:
    return float(C0_HZ * (2.0 ** (semitone_from_c0 / 12.0)))

def bounds_for(target_hz: float) -> Tuple[float, float]:
    floor = max(10.0, 0.45 * target_hz)
    ceil = max(400.0, 2.5 * target_hz)
    if ceil <= floor:
        ceil = floor * 2.0
    return floor, ceil

def impose_pitch_psola(snd: parselmouth.Sound, target_hz: float) -> parselmouth.Sound:
    floor, ceil = bounds_for(target_hz)
    m = parselmouth.praat.call(snd, "To Manipulation", TIME_STEP_S, floor, ceil)
    tier = parselmouth.praat.call(m, "Extract pitch tier")
    parselmouth.praat.call(tier, "Formula", f"{target_hz}")
    parselmouth.praat.call([tier, m], "Replace pitch tier")
    return parselmouth.praat.call(m, "Get resynthesis (overlap-add)")

def apply_fade(snd: parselmouth.Sound, fade_ms: float = FADE_MS) -> parselmouth.Sound:
    if fade_ms <= 0:
        return snd
    x = snd.values.copy()  # (1, n)
    n = x.shape[1]
    if n == 0:
        return snd
    fade_samps = int((fade_ms / 1000.0) * snd.sampling_frequency)
    fade_samps = max(1, min(fade_samps, n // 2))
    ramp_in = np.linspace(0.0, 1.0, fade_samps, endpoint=True)
    ramp_out = np.linspace(1.0, 0.0, fade_samps, endpoint=True)
    x[0, :fade_samps] *= ramp_in
    x[0, -fade_samps:] *= ramp_out
    return parselmouth.Sound(values=x, sampling_frequency=snd.sampling_frequency)

def peak_normalize(snd: parselmouth.Sound, target_peak: float = PEAK_TARGET) -> parselmouth.Sound:
    x = snd.values.copy()
    if x.size == 0:
        return snd
    peak = float(np.max(np.abs(x)))
    if peak <= 0.0:
        return snd
    gain = target_peak / peak
    x *= gain
    return parselmouth.Sound(values=x, sampling_frequency=snd.sampling_frequency)

def make_silence(seconds: float) -> parselmouth.Sound:
    seconds = max(0.0, float(seconds))
    return parselmouth.praat.call("Create Sound from formula", "Gap", 1, 0, seconds, SR, "0")
