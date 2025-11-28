The .exe build is built with pyinstaller but the code can be run directly from the source as well, provided you have a new enough Python version and the necessary modules.

The Python module praat-parselmouth is used for pitching, source can be found at https://github.com/YannickJadoul/Parselmouth.

The user interface uses wxPython. A wxFormBuilder file is provided for making changes to the UI.

This command is used to compile the code: pyinstaller --onefile --noconsole --icon=icon.ico --hidden-import numpy chromatic_gen.py