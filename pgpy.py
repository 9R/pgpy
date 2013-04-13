from flask import Flask, render_template, url_for, escape, jsonify, flash, request, redirect, abort
from flask.ext.uploads import UploadSet, IMAGES, TestingFileStorage, configure_uploads
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required
from werkzeug import check_password_hash
import os
import libpgpy
import logging

import config

#### defaults

LOG = logging.getLogger(__name__)

USERS = libpgpy.get_users('users.txt')
USER_AUTH = dict((u.name, u) for u in USERS.itervalues())

SECRET_KEY = config.py['secret']
DEBUG = True

UPLOADS_DEFAULT_DEST = 'static/'

sitename = config.py['sitename']

#### application

app = Flask(__name__)
app.config.from_object(__name__)

#### login

login_manager = LoginManager()
login_manager.anonymous_user= libpgpy.Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log"
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

#### uploads

media = UploadSet('media', IMAGES + ('mp4',) )
configure_uploads(app, media )

#### utils

@login_manager.user_loader
def load_user(id):
  return USERS.get(int(id))

#### views

@app.route('/login', methods=["POST","GET"])
def login():
  if request.method == "POST" and "username" in request.form:
    username = request.form["username"]
    password = request.form["password"]
    if username not in USER_AUTH:
      return redirect(request.form.get("next") ) 
    if check_password_hash( USER_AUTH[username].pwhash, password ):
      remember = request.form.get("remember", "no") == "yes"
      if login_user(USER_AUTH[username], remember=remember):
	flash("Logged in!")
	return redirect(request.form.get("next") )
      else:
	flash("Sorry, but you could not log in.")
    else:
      flash(u"Invalid username.")
  return redirect(request.form.get("next") ) 


@app.route('/logout')
def logout():
  logout_user()
  return redirect("/")


@app.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
  if request.method == 'POST' and 'media' in request.files:
    folder = None
    if 'folder' in request.form:
      subfolder = request.form['folder']
    for f in request.files.getlist('media'):
      #prevent dir traversal
      savepath = os.path.relpath(os.path.abspath(os.path.join(os.path.curdir,config.py['mediadir'],subfolder, f.filename)))
      if libpgpy.isValidMediaPath(savepath):
	#save file
	try:
          filename = media.save(f, subfolder)
        except UploadNotAllowed:
          flash("The upload was not allowed")
      else:
	return render_template('error.html', message='Illegal filename or path. Please try again.', sitename=sitename)
    return redirect(subfolder)

  elif request.method == 'GET':
    subs=libpgpy.getSubdirs()
    print subs
    return render_template('upload.html', sitename=sitename,subs=subs)


@app.route('/get_subs', methods=['POST','GET'])
def getsubs():
  return jsonify( subs=libpgpy.scanDir(config.py['mediadir'])[0]['subdirs'])


@app.route('/')
@app.route('/<path:directory>', methods=["GET","POST"])
def listing(directory=""):

  #check if dirs are valid
  if not os.path.isdir( config.py['mediadir'] ):
    return render_template('error.html', message='The media directory was not found at "' + config.py['mediadir'] + '". Please check permissions and your configuration.', sitename=config.py['sitename'])

  if not os.path.isdir( config.py['mediadir'] + directory ):
    abort(404)
 
#    return render_template('error.html', message='Invalid directory: "/' + directory + '". Please verify the submitted URL.' , sitename=sitename)

  #construct path
  p = config.py['mediadir']+directory
  #handle trailng slash
  if not p.endswith('/'):
    p = p + '/'
  
  #scan dir for files and subdirs
  dirs = libpgpy.scanDir(p)

  #render site
  return render_template('list.html' , md=config.py['mediadir'] , dirs=dirs, sitename=sitename)

from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html', message="404. Monkeys have stolen this page.", sitename=sitename), 404

@app.errorhandler(403)
def page_not_found(e):
  return render_template('error.html', message="403. Access forbidden.", sitename=sitename), 403

@app.errorhandler(500)
def page_not_found(e):
  return render_template('error.html', message="500. Internal error.", sitename=sitename), 500

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

