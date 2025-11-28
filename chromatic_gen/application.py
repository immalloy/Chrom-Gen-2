"""Application bootstrap for the Chromatic Scale Generator."""

from __future__ import annotations

import wx

from .gui import GeneratorGUI


def run_app() -> None:
    """Launch the wxPython application."""

    app = wx.App(False)
    frame = GeneratorGUI(None)
    frame.Show(True)
    app.MainLoop()


__all__ = ["run_app"]
