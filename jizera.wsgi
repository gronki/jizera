activate_this = '/var/www/jizera/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__ = activate_this))

from jizera import app as application
