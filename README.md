pgpy
====

Picture (and video) Gallery written with Python-Flask# pgpy
=====

Picture (and video) Gallery written with Python

## About

pgpy uses the python-flask micro framework as well a lightbox and flowplayer to display the media in an   apealing way. pgpy does not require a database. Instead it scans a media directory and its sub directories depending on the requested URL and stores the gathered data in a python dicitonary.
This dictionary is then used to populate the site template.

Additionally pgpy generates thumbnails and medium sized copies for all supported images formats and stores them in the "thumbs/" and "web/" subfolder respectively. It also generates download links and html code to to help using the media on another websites like a blog via c*p.

pgpy was modelled on ffff.at's fuckflickr (http://ffff.at/fuckflickr) but I onlu used the general concept (simple layout, no database) as inspiration and did not consult their php code.


## Dependencies
    python-flask >= 0.8
    python-imaging
    
 pip 
  
    Flask-Login
    Flask-Uploads
    


## Usage

Modify the configuration in config.py to your needs.

You can add users and generate password hashes by executing

    python adduser.py

To try pgpy instantly execute

    python pgpy.py

and access pgpg on [http://localhost:5000](http://localhost:5000)

