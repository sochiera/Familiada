# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec file for Familiada (macOS .app bundle)
# Build command:  pyinstaller familiada.spec

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('rounds',  'rounds'),
        ('sounds',  'sounds'),
        ('fonts',   'fonts'),
        ('config.ini', '.'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.display',
        'pygame.event',
        'pygame.image',
        'pygame.transform',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Familiada',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # brak okna terminala
    disable_windowed_traceback=False,
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
    name='Familiada',
)

# macOS: zbuduj .app bundle
app = BUNDLE(
    coll,
    name='Familiada.app',
    icon=None,
    bundle_identifier='pl.familiada.game',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.0',
        'CFBundleName': 'Familiada',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
    },
)
