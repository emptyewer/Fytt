# -*- mode: python -*-

block_cipher = None


a = Analysis(['fytt2.py'],
             pathex=['/home/venky/Projects/Fytt2'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='fytt2',
          debug=False,
          strip=None,
          upx=True,
          console=True )
