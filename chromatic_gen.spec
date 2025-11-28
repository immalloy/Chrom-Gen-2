# Custom PyInstaller spec to ensure all dependencies are bundled for the Windows executable.
# Build with: pyinstaller chromatic_gen.spec

from PyInstaller.building.build_main import Analysis, COLLECT, EXE, PYZ
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
    copy_metadata,
)

block_cipher = None

hiddenimports = (
    collect_submodules("numpy")
    + collect_submodules("wx")
    + collect_submodules("parselmouth")
)

# Collect binary and data assets for dependencies that ship compiled extensions or resources.
binaries = collect_dynamic_libs("parselmouth") + collect_dynamic_libs("numpy")
datas = (
    collect_data_files("parselmouth")
    + collect_data_files("wx")
    # Package is published to PyPI as "praat-parselmouth", so use the distribution
    # name here to ensure PyInstaller can locate the metadata during the build.
    + copy_metadata("praat-parselmouth")
    + [("icon.ico", ".")]
)

analysis = Analysis(
    ["chromatic_gen.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="chromatic_gen",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico",
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="chromatic_gen",
)
