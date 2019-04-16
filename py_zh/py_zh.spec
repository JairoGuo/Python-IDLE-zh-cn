# -*- mode: python -*-

block_cipher = None


a = Analysis(['py_zh.py'],
             pathex=['D:\\Project\\py_zh'],
             binaries=[],
             datas=[('idlelib.zip', 'res'),('get_py_dir.py', 'res'),('ico.ico','res')],
             hiddenimports=[],
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
          name='py_zh',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon="ico.ico" )
