'''
An implementation of Li and Mould's structure-preserving stippling algorithm.
'''

from itertools import izip

import numpy as np
from skimage.draw import circle

from priority import *
from img_util import *

def print_message(pixels_processed, pixels_total, num_stipples):
  print("Processed {0} out of {1} pixels. Made {2} stipples."
        .format(pixels_processed, pixels_total, num_stipples))

class Stippler:
  def __init__(self, Gn=5.0, Gp=5.0, k=0.1, D=7.0, thresh=127, rmin=1.0,
                     rmax=2.0, b=2.0, clip_min=1, clip_max=254):
    self.queue = PriorityQueue()
    self.thresh = thresh
    self.rmin = rmin
    self.rmax = rmax
    self.D = D
    self.b = b
    self.Gn = Gn
    self.Gp = Gp
    self.k = k
    self.clip_min = clip_min
    self.clip_max = clip_max

  def calculate_stipple_size(self, intensity):
    return self.rmin + (self.rmax-self.rmin)*(255-intensity) / 255.0

  def get_stipples(self, image):
    img = image.astype(float)
    self.queue.build(img)
    processed = np.zeros_like(img, dtype=bool)

    stipples = []

    i = 0
    while not self.queue.empty():
      (x, y, p) = self.queue.pop()
      if processed[y,x] or p != get_priority(img[y,x]):
        continue

      r = self.calculate_stipple_size(image[y,x])

      if img[y,x] <= self.thresh:
        app = 0
        stipples.append( (x,y,r) )
      else:
        app = 255

      err = img[y,x] - app
      processed[y,x] = True
      self.distribute_error(img, x, y, r, err, processed)

      i += 1
      if i % 1000 == 0:
        print_message(i, image.size, len(stipples))

    print_message(i, image.size, len(stipples))
    return stipples

  def get_mask(self, x, y, processed):
    rows, cols = circle(y, x, self.D/2, processed.shape)
    npix = len(rows)
    ind = [i for i in range(npix) if not processed[rows[i],cols[i]]]
    return rows[ind], cols[ind]

  def calculate_weight(self, x, y, img, err, rows, cols):
    dy = rows-y
    dx = cols-x
    dist2 = (dx*dx+dy*dy).astype(float)

    if err > 0:
      w = img[rows,cols] / (dist2 ** (0.5*self.b))
    else:
      w = (255-img[rows,cols]) / (dist2 ** (0.5*self.b))
    wtot = np.sum(w)
    if wtot > 0:
      w /= wtot

    return w

  def calculate_gamma_correction(self, r, err):
    if err < 0:
      return (1/r) ** self.Gn
    else:
      return r ** self.Gp

  def calculate_extra_error(self, r, err):
    if err > 0:
      return (np.pi*r*r-1)*self.k
    else:
      return 0.0

  def distribute_error(self, img, x, y, r, err, processed):
    rows, cols = self.get_mask(x, y, processed)
    if len(rows) == 0:
      return

    w = self.calculate_weight(x, y, img, err, rows, cols)
    s = self.calculate_gamma_correction(r, err)
    e0 = self.calculate_extra_error(r, err)
    img[rows,cols] += s*(err+e0)*w
    img[rows,cols] = np.clip(img[rows,cols], self.clip_min, self.clip_max)
    for (row,col) in izip(rows,cols):
      self.queue.push(col, row, img)

def stipple(imgfile, svgfile, Gn=5.0, Gp=5.0, k=0.1, D=7.0, thresh=127,
            rmin=1.0, rmax=2.0, b=2.0, clip_min=1, clip_max=254):
  '''Read from an image file and saves the stipples in an SVG file.'''

  image = load_image(imgfile)

  stippler = Stippler(Gn, Gp, k, D, thresh, rmin, rmax, b, clip_min, clip_max)
  stipples = stippler.get_stipples(image)

  height, width = image.shape
  save_svg(stipples, width, height, svgfile)


