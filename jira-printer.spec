# -*- mode: python -*-
import os

path = os.getcwd()

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=[path,
             path + '\\jira_printer'],
             binaries=[],
             datas=[
             (path + '\\jira_printer\\icons\\*.png', 'icons'),
             (path + '\\jira_printer\\icons\\*.png', 'icons'),
             (path + '\\jira_printer\\templates\\*.html.j2', 'templates'),
             (path + '\\jira_printer\\files\\*.txt', 'files'),
             (path + '\\jira_printer\\files\\Jira_Printer_help.pdf', 'files')],
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
          name='Jira_Printer',
          debug=False,
          strip=False,
          upx=True,
          icon=path + '\\jira_printer\\icons\\icon.ico',
          runtime_tmpdir=None,
          console=False)
