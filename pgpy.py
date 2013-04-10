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

  dirs=[]
  #construct path
  p = config.py['mediadir']+directory
  #handle trailng slash
  if not p.endswith('/'):
    p = p + '/'

  for d in os.walk(p) :

    path=d[0].encode('utf-8')

    #ignore thumb and web sub-dirs
    if not (path.endswith('thumbs') or path.endswith('web') ):

      if not path.endswith('/'):
        path = path + '/'

      #create thumb and web sub-dirs if needed
      for sub in ['thumbs', 'web']:
        if not os.path.isdir(path+sub):
	  os.mkdir(path+sub)

      #create empty file list for current dir
      files = []

      #save stats for every file in dict
      for f in d[2]:
	suffix = f.lower()[-3:]
	LOG.info(suffix)
        if  suffix in config.py['supported_file']:
	  f = f.encode("utf-8")
  	  files.append({'name': f , 'mtime': os.path.getmtime(path+'/'+f) })

	  #create thumbs if necessary
	  if not os.path.isfile(path+'thumbs/'+f):
	    libpgpy.resizePic2( path + f, (config.py['thumbres'], config.py['thumbres'])).save(path + 'thumbs/' + f)

	  #create websize if necessary
	  if not os.path.isfile(path+'web/'+f):
            libpgpy.resizePic2( path + f, (config.py['webres'], config.py['webres'])).save(path + 'web/' + f)

      #remove thumb and web from subdir listing
      try:
	d[1].remove('web')
      except:
	pass
      try:
	d[1].remove('thumbs')
      except:
	pass

      #empty list of subdirs
      subdirs = []
      
      for subdir in d[1]:
	subdirs.append(subdir.replace(config.py['mediadir'], ''))

      #save dir stats in dict
      dirs.append({'dir': path.replace(config.py['mediadir'], '') , 'subdirs':subdirs , 'files': files })

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

