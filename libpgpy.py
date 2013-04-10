import Image
import ImageOps



def resizePic(  pic, res ):
  i = Image.open(pic)
  return i.resize(res, Image.NEAREST)

def resizePic2( pic, res ):
  i = Image.open(pic)
  return ImageOps.fit(i, res )
