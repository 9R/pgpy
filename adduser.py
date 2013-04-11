from werkzeug import generate_password_hash
import getpass
from sys import exit

userfile = 'users.txt'

username = raw_input('Enter username:')

f = open(userfile, "a+")
for line in f.readlines():
  if line.split(' ')[0] == username:
    f.close()
    exit( 'Username already exists')

pw1= getpass.getpass('Enter password:')
pw2= getpass.getpass('Confirm password:')
if pw1 == pw2:
  pwhash = generate_password_hash(pw1)
else:
  exit( 'Your input did not match.')
if len(pw1) == 0:
  exit("you did not enter a password")
elif len(pw1) < 8 :
  confirm = getpass.getpass('your password is quite short. If you are sure you want to use it enter a "yes" in upper case.')
  if confirm != "YES":
    exit("Aborting.")
f.write(username + ' ' + pwhash + '\n')
f.close()
print ('User "'+ username + '" was add to '+ userfile+'.')

