# -*- mode: python ; coding: utf-8 -*-

import sys
from os import path

block_cipher = None

site_packages = next(p for p in sys.path if 'site-packages' in p)

a = Analysis(['FinalCif/finalcif.py'],
             pathex=['/Users/daniel/Documents/GitHub/FinalCif'],
             binaries=[],
             datas=[('./FinalCif/gui', 'gui'), (path.join(site_packages,"docx","templates"), 'docx/templates'),
                    ('./FinalCif/template', 'template'), ('FinalCif/icon', 'icon'), ('FinalCif/displaymol', 'displaymol')],
             hiddenimports=['FinalCif.tools.misc', 'FinalCif.tools.settings', 'FinalCif.datafiles', 'gemmi', 'qtawesome'],
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
          icon='FinalCif/icon/finalcif2.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

app = BUNDLE(exe,
             name='Finalcif-v_macos.app',
             icon='FinalCif/icon/finalcif2.ico',
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True'
             },
             )
