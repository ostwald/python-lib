import sys, math
from pallete import pallete
from HyperText.HTML40 import *

# see http://www.compuphase.com/cmetric.htm
class RGB:
	def __init__(self, rgb):
		self.red = rgb[0]
		self.green = rgb[1]
		self.blue = rgb[2]

	def delta (self, other):
		rmean = float(self.red + other.red)/2
		r = self.red - other.red
		g = self.green - other.green
		b = self.blue - other.blue

		return math.sqrt ( (2 + (rmean/256)) * r**2 + 4 + g**2 + (2 + ((255-rmean)/256)) * b**2 )
		
	def altDelta (self, other):
		rmean = (long(self.red) + long(other.red))/2
		r = long(self.red) - long(other.red)
		g = long(self.green) - long(other.green)
		b = long(self.blue) - long(other.blue)

		return math.sqrt ((((512+rmean) *r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))
		
	def __repr__ (self):
		return 'RGB (%d, %d, %d)' % (self.red, self.green, self.blue)

class ColorMatcher():
	
	def __init__ (self):
		self.colors=[]
		for rgb in pallete:
			self.colors.append(RGB (rgb))
			
	def match (self, color):
		minDelta = 100000
		closest = None
		for rgb in self.colors:
			delta = rgb.delta (color)
			print '%s - %f' % (rgb, delta)
			if delta < minDelta:
				minDelta = delta
				closest = rgb
				
		return closest

def basicColorTesters ():
	colors = [];add=colors.append
	for rgb in pallete:
		add (RGB (rgb))
		
	for color in colors:
		print 'r:%d, g:%d, b:%d' % (color.red, color.green, color.blue)
		
	print colors[0].delta(colors[1])
	
	base = colors[0]
	for color in colors[1:]:
		print base.delta(color)
		
if __name__ == '__main__':
	matcher = ColorMatcher()
	
	if 1:
		match = matcher.match(RGB ((0, 0, 256)))
		print match
	else:
		#find delta between two colors
		print 'first color: %s' % matcher.colors[0]
		print 'second color: %s' % matcher.colors[1]
		print 'delta: %f' % matcher.colors[0].delta(matcher.colors[1])
		
