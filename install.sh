jizera_path='/var/www/jizera'

sudo cp jizera.conf /etc/httpd/conf.d/
sudo cp jizera.wsgi "$jizera_path"

source "$jizera_path/venv/bin/activate"
python setup.py install

sudo systemctl reload httpd
sudo systemctl restart httpd