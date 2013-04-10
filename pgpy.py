from flask import Flask, render_template, url_for, escape, jsonify
import os
import time
import libpgpy
import logging

import config

app = Flask(__name__)

LOG = logging.getLogger(__name__)

@app.route('/')
@app.route('/<path:directory>')
def listing(directory=""):

  #check if dirs are valid
  if not os.path.isdir( config.py['mediadir'] ):
    return render_template('error.html', message='The media directory was not found at "' + config.py['mediadir'] + '". Please check permissions and your configuration.', sitename=config.py['sitename'])

  if not os.path.isdir( config.py['mediadir'] + directory ):
    return render_template('error.html', message='Invalid directory: "/' + directory + '". Please verify the submitted URL.' , sitename=config.py['sitename'])

#  dirs=[]
  #construct path
  p = config.py['mediadir']+directory
  #handle trailng slash
  if not p.endswith('/'):
    p = p + '/'
  
  #scan dir for files and subdirs
  dirs = libpgpy.scanDir(p)

  #render site
  return render_template('list.html' , md=config.py['mediadir'] , dirs=dirs, sitename=config.py['sitename'])




@app.route('/favicon.ico')
def favicon():
  return url_for('static', filename='favicon.ico')

##serve static links to jpgs
@app.route('/<path>.jpg')
def picserv(path):
  return url_for('static', filename="/"+ path +".jpg")


if __name__ == '__main__':
  app.debug=True
  app.run('0.0.0.0')

if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

