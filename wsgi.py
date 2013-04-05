import sys, logging, os

logging.basicConfig(stream=sys.stderr)

os.chdir('/var/www/pyfflik')
sys.path.insert(0, '/var/www/pyfflik')

from pyfflik import app
application = app
