# path to the application
jizera_path = '/home/gronki/jizerazero'

# activate the virtual environment
activate_this = jizera_path + '/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__ = activate_this))

# insert application path so no need to install it into venv
import sys
sys.path.insert(0, jizera_path)
import os
os.chdir(jizera_path)

# import
from jizerazero import app as application
