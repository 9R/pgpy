import Image
import ImageOps
import config
import os

def resizePic(  pic, res ):
  i = Image.open(pic)
  return i.resize(res, Image.NEAREST)

def resizePic2( pic, res ):
  i = Image.open(pic)
  return ImageOps.fit(i, res )

def scanDir (path):
  """
  Scans subdirs and files in path and returns a list 
  of dict for each directory.
  
  example for these dicts:
  {'files':[{'name': 'filename.jpg', 'date': mtime }, 'subdirs':[], 'dir':'']}
  """
  dirs =[]
  for d in os.walk(path) :

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
        if  suffix in config.py['supported_file']:
          f = f.encode("utf-8")
          files.append({'name': f , 'mtime': os.path.getmtime(path+'/'+f) })

          #create thumbs if necessary
          if not os.path.isfile(path+'thumbs/'+f):
            resizePic2( path + f, (config.py['thumbres'], config.py['thumbres'])).save(path + 'thumbs/' + f)

          #create websize if necessary
          if not os.path.isfile(path+'web/'+f):
            resizePic2( path + f, (config.py['webres'], config.py['webres'])).save(path + 'web/' + f)

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

  return dirs
