# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['zalo-gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime',
        'pandas',
        'selenium',
        'pyautogui',
        'webdriver_manager',
        'webdriver_manager.firefox',
        'webdriver_manager.chrome',
        'webdriver_manager.microsoft',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add streamlit-related files
import streamlit
import streamlit.web.cli
import os
import shutil
from pathlib import Path

streamlit_path = os.path.dirname(streamlit.__file__)
a.datas += Tree(streamlit_path, prefix='streamlit')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Zalo Automation Tool',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='zalo_app',
)
