class SVG:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.elements = []
  
  def add(self, element):
    self.elements.append(element)

  def create(self):
    return '<svg width="{0.width}" height="{0.height}">\n  {1}\n</svg>\n'.format(
             self, '\n  '.join(elem.tag() for elem in self.elements))

  def save(self, filename):
    with open(filename, 'w') as f:
      f.write(self.create())

class SVGCircle:
  def __init__(self, cx, cy, r, stroke="black", width="1", fill="black"):
    self.cx = cx
    self.cy = cy
    self.r = r
    self.stroke = stroke
    self.width = width
    self.fill = fill

  def tag(self):
    return '<circle cx="{0.cx}" cy="{0.cy}" r="{0.r:.03f}" stroke="{0.stroke}" ' \
            'stroke-width="{0.width}" fill="{0.fill}" />'.format(self)


