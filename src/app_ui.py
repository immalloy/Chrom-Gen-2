import wx

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
OCTAVES = [str(i) for i in range(0, 9)]  # 0..8

class AppFrame(wx.Frame):
    def __init__(self, parent=None, title="Chromatic Generator", size=(560, 420)):
        super().__init__(parent, title=title, size=size)
        panel = wx.Panel(self)

        # Directory
        dir_label = wx.StaticText(panel, label="Samples Folder (1.wav, 2.wav, ...):")
        self.dirPicker = wx.DirPickerCtrl(panel, style=wx.DIRP_DEFAULT_STYLE)

        # Gap + Range
        gap_label = wx.StaticText(panel, label="Gap (seconds):")
        self.gapInput = wx.TextCtrl(panel, value="0.15")
        range_label = wx.StaticText(panel, label="Range (semitones):")
        self.rangeInput = wx.TextCtrl(panel, value="25")  # C0..C2 by default

        # Start note/octave
        start_note_label = wx.StaticText(panel, label="Start Note:")
        self.startNoteChoice = wx.Choice(panel, choices=NOTES)
        self.startNoteChoice.SetSelection(0)  # C
        start_oct_label = wx.StaticText(panel, label="Start Octave:")
        self.startOctaveChoice = wx.Choice(panel, choices=OCTAVES)
        self.startOctaveChoice.SetSelection(2)  # C2 by default

        # Options
        self.randomizeCheck = wx.CheckBox(panel, label="Randomize source sample per note")
        self.pitchedCheck = wx.CheckBox(panel, label="Impose pitch (PSOLA)")
        self.pitchedCheck.SetValue(True)
        self.samplesCheck = wx.CheckBox(panel, label="Export per-note WAVs to /pitched_samples")

        # Buttons
        self.generateBtn = wx.Button(panel, label="Generate Chromatic")
        self.quitBtn = wx.Button(panel, label="Quit")

        # Layout
        s = wx.BoxSizer(wx.VERTICAL)
        gs = wx.FlexGridSizer(rows=5, cols=2, vgap=8, hgap=8)
        gs.AddMany([
            (dir_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.dirPicker, 1, wx.EXPAND),
            (gap_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.gapInput, 0, wx.EXPAND),
            (range_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.rangeInput, 0, wx.EXPAND),
            (start_note_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.startNoteChoice, 0, wx.EXPAND),
            (start_oct_label, 0, wx.ALIGN_CENTER_VERTICAL), (self.startOctaveChoice, 0, wx.EXPAND),
        ])
        gs.AddGrowableCol(1, 1)

        s.Add(gs, 0, wx.ALL | wx.EXPAND, 12)
        s.Add(self.randomizeCheck, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        s.Add(self.pitchedCheck, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        s.Add(self.samplesCheck, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        btns = wx.BoxSizer(wx.HORIZONTAL)
        btns.AddStretchSpacer(1)
        btns.Add(self.generateBtn, 0, wx.RIGHT, 8)
        btns.Add(self.quitBtn, 0)

        s.Add(btns, 0, wx.ALL | wx.EXPAND, 12)
        panel.SetSizerAndFit(s)
        self.Centre()