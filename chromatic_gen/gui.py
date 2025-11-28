"""GUI implementation for the chromatic scale generator."""
from __future__ import annotations

from pathlib import Path

import wx

from chromatic_gen import app_ui
from chromatic_gen.generation import SampleSetEmptyError, generate_chromatic_scale


class GeneratorGUI(app_ui.AppFrame):
    def generate_chromatic(self, event):
        sample_path = Path(self.dirPicker.GetPath())
        gap_seconds = float(self.gapInput.GetValue())
        semitones = int(self.rangeInput.GetValue())
        start_note_index = self.startNoteChoice.GetSelection()
        start_octave_value = int(self.startOctaveChoice.GetStringSelection())
        pitched = self.pitchedCheck.IsChecked()
        dump_samples = self.samplesCheck.IsChecked()

        try:
            generate_chromatic_scale(
                sample_path,
                semitones,
                gap_seconds,
                start_note_index,
                start_octave_value,
                pitched,
                dump_samples,
            )
            wx.MessageBox("Chromatic scale generated successfully.", "Success", wx.ICON_INFORMATION)
        except SampleSetEmptyError as error:
            wx.MessageBox(str(error), "Missing samples", wx.ICON_ERROR)
        except Exception as error:  # noqa: BLE001
            wx.MessageBox(str(error), "Generation failed", wx.ICON_ERROR)


__all__ = ["GeneratorGUI"]
