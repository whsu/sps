import warnings

from skimage import img_as_ubyte
from skimage.io import imread

from svg_util import *

def load_image(imgfile):
  image = imread(imgfile, as_grey=True)
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    image = img_as_ubyte(image)
  return image

def save_svg(stipples, width, height, svgfile):
  svg = SVG(width, height)
  for x,y,r in stipples:
    svg.add(SVGCircle(x,y,0.5*r))
  svg.save(svgfile)

