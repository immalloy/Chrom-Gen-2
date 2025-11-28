# Building a standalone Windows executable

This repository includes a PyInstaller spec (`chromatic_gen.spec`) that bundles
all dependencies (including `numpy`, `wxPython`, and `parselmouth`) into a
foldered distribution so the app can run on Windows without a local Python
installation.

## Prerequisites
- Python 3.10 or later
- `pip install -r requirements.txt` (or at least `pyinstaller`, `numpy`,
  `wxPython`, and `praat-parselmouth`)

## Build steps
1. Install PyInstaller: `pip install pyinstaller`
2. From the repository root, run:
   ```
   pyinstaller chromatic_gen.spec
   ```
3. The bundled app will be available in `dist/chromatic_gen/chromatic_gen.exe`
   along with the required DLLs and support files.

The spec file pre-collects all submodules, binary extensions, and metadata
needed by the dependencies so PyInstaller won't miss components like `numpy` or
Parselmouth's native libraries.
