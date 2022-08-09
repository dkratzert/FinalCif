# -*- mode: python ; coding: utf-8 -*-

import sys
from os import path

block_cipher = None
site_packages = next(p for p in sys.path if 'site-packages' in p)

a = Analysis(['./finalcif/finalcif_start.py'],
             pathex=['/Users/daniel/Documents/GitHub/FinalCif', '.'],
             binaries=[],
             datas=[('finalcif/gui', 'gui'),
                    (path.join(site_packages, "docx", "templates"), 'finalcif/docx/templates'),
                    ('finalcif/template', 'template'), ('finalcif/icon', 'icon'),
                    ],
             hiddenimports=['tools', 'tools.misc', 'tools.settings', 'datafiles', 'gemmi', 'qtawesome', 'finalcif',
                            'finalcif.app_path', 'numpy'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FinalCif',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='finalcif/icon/finalcif2.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)

