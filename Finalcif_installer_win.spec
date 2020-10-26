# -*- mode: python ; coding: utf-8 -*-

import sys
from os import path

block_cipher = None
site_packages = next(p for p in sys.path if 'site-packages' in p)

a = Analysis(['finalcif.py'],
             pathex=['.'],
             binaries=[('update.exe', '.')],
             datas=[('./gui', 'gui'), (path.join(site_packages,"docx","templates"), 'docx/templates'), 
                    ('./template', 'template'), ('icon', 'icon'), ('displaymol', 'displaymol'), ('tools', 'tools'),
                    ],
             hiddenimports=['tools', 'tools.misc', 'tools.settings', 'datafiles', 'gemmi', 'qtawesome', 'finalcif'],

                    ('./template', 'template'), ('icon', 'icon'), ('displaymol', 'displaymol'), ('tools', 'tools')
                    ],
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
          icon='icon/finalcif2.ico',
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FinalCif')
