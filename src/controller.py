import os
import random
from typing import List
import wx
import parselmouth

from app_ui import AppFrame
from audio_processing import (
    load_mono,
    hz_from_c0,
    impose_pitch_psola,
    apply_fade,
    peak_normalize,
    make_silence,
)

class Controller(AppFrame):
    def __init__(self):
        super().__init__(None)
        self.generateBtn.Bind(wx.EVT_BUTTON, self.on_generate)
        self.quitBtn.Bind(wx.EVT_BUTTON, lambda evt: self.Close(True))

    def _err(self, msg: str):
        wx.MessageBox(msg, "Error", wx.OK | wx.ICON_ERROR)

    def _ok(self, msg: str):
        wx.MessageBox(msg, "Done", wx.OK | wx.ICON_INFORMATION)

    def _count_numbered_wavs(self, base_dir: str) -> int:
        i = 0
        while os.path.exists(os.path.join(base_dir, f"{i+1}.wav")):
            i += 1
        return i

    def on_generate(self, _evt):
        try:
            folder = self.dirPicker.GetPath()
            gap_s = float(self.gapInput.GetValue())
            steps = int(self.rangeInput.GetValue())
            start_note = int(self.startNoteChoice.GetSelection())   # 0..11
            start_oct = int(self.startOctaveChoice.GetSelection())  # 0..8
            randomize = bool(self.randomizeCheck.IsChecked())
            pitched = bool(self.pitchedCheck.IsChecked())
            export_samples = bool(self.samplesCheck.IsChecked())
        except Exception:
            self._err("Invalid inputs.")
            return

        if not folder or not os.path.isdir(folder):
            self._err("Pick a valid folder with numbered samples (1.wav, 2.wav, ...).")
            return
        if steps <= 0:
            self._err("Range must be ≥ 1.")
            return

        file_count = self._count_numbered_wavs(folder)
        if file_count == 0:
            self._err("No source samples found.")
            return

        try:
            silence = make_silence(gap_s)
        except Exception:
            self._err("Failed to create silence.")
            return

        start_key_from_c0 = start_note + 12 * start_oct  # C0->0, C1->12, C2->24
        if start_key_from_c0 < 0:
            self._err("Start below C0 is not supported.")
            return

        notes: List[parselmouth.Sound] = []
        sequence: List[parselmouth.Sound] = []

        for i in range(steps):
            src_idx = random.randint(1, file_count) if randomize else ((i % file_count) + 1)
            src_path = os.path.join(folder, f"{src_idx}.wav")

            try:
                base = load_mono(src_path)
            except Exception:
                self._err(f"Failed to load {src_path}")
                return

            if pitched:
                target_hz = hz_from_c0(start_key_from_c0 + i)  # exact ET, C0-safe
                note = impose_pitch_psola(base, target_hz)
            else:
                note = base

            note = apply_fade(note)
            note = peak_normalize(note)

            notes.append(note)
            sequence.append(note)
            sequence.append(silence)

        try:
            chrom = parselmouth.Sound.concatenate(sequence)
            chrom.save(os.path.join(folder, "chromatic.wav"), "WAV")
        except Exception:
            self._err("Failed to save chromatic.wav")
            return

        if export_samples and pitched:
            out_dir = os.path.join(folder, "pitched_samples")
            try:
                os.makedirs(out_dir, exist_ok=True)
                for n, s in enumerate(notes, start=1):
                    s.save(os.path.join(out_dir, f"pitched_{n}.wav"), "WAV")
            except Exception:
                self._err("Failed to save pitched samples.")
                return

        self._ok("Chromatic generated (C0/C1 ready).")

