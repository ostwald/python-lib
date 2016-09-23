"""
Connects

Thisi is the Connects element
<Connects>
	<Connect  FromSheet="3" FromPart="9" ToSheet="1" ToPart="102"/>
	<Connect FromSheet="3" FromPart="12" ToSheet="2" ToPart="103"/>
</Connects>

Here the line is Sheet3, which connects 
- it's beginning (FromPart 9) to connector 2 (ToPart 102) of Sheet1 (rectangle 1)
- it's end (FromPart 12) to connector 3 (ToPart 102) of Sheet 2 (rectangle 2)

"""
import os, sys
from JloXml import XmlRecord, XmlUtils

class Connects:

	def __init__ (self, line, fromShape, fromConnector, toShape, toConnector):
		"""
		line, fromShape, toShape are shape IDs
		from and toConnector are connector IDs
		"""
		self.element = XmlUtils.createElement('Connects')
		# connect begining of line to connector on fromShape
		connect1 = XmlUtils.createElement('Connect')
		connect1.setAttribute ('FromSheet', str(line))
		connect1.setAttribute ('FromPart', '9')
		connect1.setAttribute ('ToSheet', str(fromShape))
		connect1.setAttribute ('ToPart', '10%s' % fromConnector)
		self.element.appendChild(connect1)
		
		# connect end of line to connector on toShape
		connect2 = XmlUtils.createElement('Connect')
		connect2.setAttribute ('FromSheet', str(line))
		connect2.setAttribute ('FromPart', '12')
		connect2.setAttribute ('ToSheet', str(toShape))
		connect2.setAttribute ('ToPart', '10%s' % toConnector)
		self.element.appendChild(connect2)
		
	def __repr__ (self):
		return self.element.toxml()
		
if __name__ == '__main__':
	c = Connects(3, 1, 2, 2, 3)
	print c
