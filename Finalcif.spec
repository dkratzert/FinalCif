# -*- mode: python -*-

# pyinsatller Finalcif.spec --clean -w
#.\venv\Scripts\pyinstaller.exe -w --clean scripts\Finalcif.spec
# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec
# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -D     # one dir

# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F     # one file
# copy dist\FinalCif.exe W:\htdocs\finalcif


import sys
from os import path

block_cipher = None
site_packages = next(p for p in sys.path if 'site-packages' in p)

a = Analysis(['./finalcif.py'],
             pathex=['D:\\Programme\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64', 'D:\\GitHub\\FinalCif'],
             binaries=[],
             #datas=[],
             datas=[('./gui', 'gui'), (path.join(site_packages,"docx","templates"), 'docx/templates'), 
                    ('./template', 'template')],
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
          name='FinalCif',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          icon='icon\\multitable.ico',
          console=True)

