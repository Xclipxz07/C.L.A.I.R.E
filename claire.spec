# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for C.L.A.I.R.E

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('config.example.yaml', '.'),
    ],
    hiddenimports=[
        'backend',
        'backend.core',
        'backend.core.config',
        'backend.core.assistant',
        'backend.skills',
        'backend.skills.base',
        'backend.skills.weather',
        'backend.skills.system',
        'backend.ui',
        'backend.ui.terminal_ui',
        'backend.ui.gui',
        'backend.voice',
        'yaml',
        'requests',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Claire',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Claire',
)
