REMOTE_HOST='galaktyka.duckdns.org'

rsync -rv \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  --exclude="*.egg" \
  jizera setup.py jizera.conf jizera.wsgi install.sh \
  $REMOTE_HOST:jizera-install/

ssh -t $REMOTE_HOST 'cd jizera-install && ./install.sh'