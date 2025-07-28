# -*- mode: python ; coding: utf-8 -*-

import sys
from os import path
#pyinstaller myapp.py --noconfirm --onedir --hidden-import PySide6.QtWebEngineWidgets --exclude-module PySide6.QtMultimedia

block_cipher = None
site_packages = next(p for p in sys.path if 'site-packages' in p)

a = Analysis(['finalcif/finalcif_start.py'],
             pathex=['finalcif'],
             binaries=[('update.exe', '.')],
             datas=[('finalcif/gui', 'gui'),
                    (path.join(site_packages, "docx", "templates"), 'finalcif/docx/templates'),
                    ('finalcif/template', 'template'), ('finalcif/icon', 'icon'),
                    # Copies also the missing files from enchant to the distributions enchant directory:
                    ((path.join(site_packages, "enchant")), ('enchant'))
                    ],
             hiddenimports=['tools', 'tools.misc', 'tools.settings', 'datafiles', 'gemmi', 'qtawesome', 'finalcif',
                            'finalcif.app_path', 'numpy', 'enchant'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='FinalCif',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='finalcif/icon/finalcif2.ico',
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FinalCif')
