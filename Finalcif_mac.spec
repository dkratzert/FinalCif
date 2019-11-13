# -*- mode: python ; coding: utf-8 -*-

import sys
from os import path

block_cipher = None

site_packages = next(p for p in sys.path if 'site-packages' in p)

a = Analysis(['finalcif.py'],
             pathex=['/Users/daniel/GitHub/FinalCif'],
             binaries=[],
             datas=[('./gui', 'gui'), (path.join(site_packages,"docx","templates"), 'docx/templates'),
                    ('./template', 'template'), ('icon', 'icon')],
             hiddenimports=['tools.misc', 'tools.settings', 'datafiles', 'gemmi'],
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
          name='finalcif',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='icon/finalcif2.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

app = BUNDLE(exe,
             name='finalcif.app',
             icon='icon/finalcif2.ico',
             bundle_identifier=None)
