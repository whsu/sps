'''
A simple priority queue for pixels. Each pixel has an integer intensity
between 0 (black) and 255 (white). Pixels closer to the ends of the 
spectrum have higher priority than pixels closer to the middle.
'''

from heapq import *

def get_priority(intensity):
	return min(intensity, 255-intensity)

class PriorityQueue:
	def __init__(self, image=None):
		self.queue = []

		if image is not None:
			self.build(image)

	def build(self, image):
		(ny, nx) = image.shape
		for y in xrange(ny):
			for x in xrange(nx):
				self.push(x, y, image)

	def push(self, x, y, image):
		heappush(self.queue, (get_priority(image[y,x]), (x,y)))

	def pop(self):
		(p, loc) = heappop(self.queue)
		(x, y) = loc
		return (x, y, p)

	def empty(self):
		return len(self.queue) == 0


