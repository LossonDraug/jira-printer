# -*- mode: python -*-
import os

path = os.getcwd()

block_cipher = None


a = Analysis(['main.py'],
             pathex=[path + '\\jira_printer\\jira-printer'],
             binaries=[],
             datas=[
             (path + '\\jira-printer\\icons\\*.png', 'icons'),
             (path + '\\jira-printer\\templates\\*.html.j2', 'templates')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Jira Printer',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False)
