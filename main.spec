# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['J:\OFFICE WORK\OBSTrigger\venv\Lib\site-packages\toml', 'J:\OFFICE WORK\OBSTrigger\venv\Lib\site-packages\obsws_python\__init__.py', 'J:\OFFICE WORK\OBSTrigger\venv\Lib\site-packages\flask\__init__.py'],
    binaries=[],
    datas=[('J:\\OFFICE WORK\\OBSTrigger\\config.toml', '.'), ('J:\\OFFICE WORK\\OBSTrigger\\scenarios.json', '.'), ('J:\OFFICE WORK\OBSTrigger\icon.png', '.')],
    hiddenimports=['toml', 'obsws_python', 'flask','pystray'],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name='main',
)
