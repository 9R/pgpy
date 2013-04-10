import sys, logging, os

logging.basicConfig(stream=sys.stderr)

os.chdir('/var/www/pgpy')
sys.path.insert(0, '/var/www/pgpy')

from pgpy import app
application = app
