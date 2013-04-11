from flask import (Flask, render_template, url_for, escape, jsonify, flash, request,
    		  redirect)
from flask.ext.login import (LoginManager, current_user, login_required,                             
                            login_user, logout_user, UserMixin, AnonymousUser,
			    confirm_login, fresh_login_required)
from werkzeug import check_password_hash
import os
import libpgpy
import logging

import config

USERS = libpgpy.get_users('users.txt')

USER_AUTH = dict((u.name, u) for u in USERS.itervalues())

app = Flask(__name__)

SECRET_KEY = config.py['secret']
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user= libpgpy.Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log"
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
  return USERS.get(int(id))

login_manager.setup_app(app)
LOG = logging.getLogger(__name__)


LOG.error(USERS[1].name)

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


@app.route('/')
@app.route('/<path:directory>', methods=["GET","POST"])
def listing(directory=""):

  #check if dirs are valid
  if not os.path.isdir( config.py['mediadir'] ):
    return render_template('error.html', message='The media directory was not found at "' + config.py['mediadir'] + '". Please check permissions and your configuration.', sitename=config.py['sitename'])

  if not os.path.isdir( config.py['mediadir'] + directory ):
    return render_template('error.html', message='Invalid directory: "/' + directory + '". Please verify the submitted URL.' , sitename=config.py['sitename'])

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

