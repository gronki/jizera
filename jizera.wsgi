import sys
import os

# path to the application
jizera_path = '/var/www/jizera'
venv_path = os.path.join(jizera_path, 'venv', 'bin')

# insert application path so no need to install it into venv
sys.path.insert(0, jizera_path)
sys.path.insert(0, venv_path)
os.chdir(jizera_path)

# import
from jizera import app as application
