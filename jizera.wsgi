import sys
import os

# path to the application
jizera_path = '/var/www/jizera'
os.chdir(jizera_path)

# import
from jizera import app as application
