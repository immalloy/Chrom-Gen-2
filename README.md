# Chromatic Scale Generator

A wxPython-based GUI that generates chromatic scales from numbered audio samples using [Parselmouth](https://github.com/YannickJadoul/Parselmouth).

## Project structure

- `chromatic_gen/`
  - `app_ui.py`: Generated wxFormBuilder layout for the application window.
  - `application.py`: wxPython bootstrap that creates and runs the GUI frame.
  - `generation.py`: Core helpers for pitching samples and assembling a chromatic scale.
  - `gui.py`: Event handlers and runtime wiring for the GUI.
- `chromatic_gen.py`: Entry point that launches the GUI with `python chromatic_gen.py` or `python -m chromatic_gen`.
- `form.fbp`: wxFormBuilder source for modifying the UI.
- `icon.ico`: Application icon used by the PyInstaller build.

## Running from source

Ensure Python 3 with the `wxPython` and `praat-parselmouth` packages installed, then run:

```bash
python chromatic_gen.py
```

## Packaging

Build a directory-based bundle with PyInstaller (default behavior) so the generated assets live alongside the executable:

```bash
pyinstaller --noconsole --icon=icon.ico --hidden-import numpy chromatic_gen.py
```

The output will appear in `dist/chromatic_gen/` (or `dist/chromatic_gen/chromatic_gen.exe` on Windows) with supporting files in the same folder.
