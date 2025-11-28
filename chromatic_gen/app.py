"""Application bootstrap helpers for the Chromatic Scale Generator."""
from __future__ import annotations

import wx

from chromatic_gen.gui import GeneratorGUI


def create_app() -> wx.App:
    """Create the wxPython application instance."""
    return wx.App(False)


def run_app() -> None:
    """Launch the GUI and enter the wxPython main loop."""
    app = create_app()
    frame = GeneratorGUI(None)
    frame.Show(True)
    app.MainLoop()


__all__ = ["create_app", "run_app"]
