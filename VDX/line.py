"""
Line - a specialization of Shape

The only hard part is computing XForm1D 

<XForm1D>
	<BeginX>3</BeginX>
	<BeginY>7.180555555555555</BeginY>
	<EndX>3.999999814563327</EndX>
	<EndY>7.180555555555555</EndY>
</XForm1D>

These should match the connections on the objects
which we get from ....

"""

from shape import Shape
import util

class Line (Shape):
	
	component_xml = util.getTemplate('LINE-PARTS')
	
	def injectComponents (self):
		"""
		the base Shape class inserts the Geom elements
		"""
		Shape.injectComponents(self);
		
		#Layout can be inserted as is. It goes before textXFormNode
		layout = self.components['Layout']
		if not layout:
			raise DomException, "Layout not found in components"

		textXFormNode = self.selectSingleNode(self.dom, 'Shape/TextXForm');
		if not textXFormNode:
			raise DomException ("TextXForm not found in Shape");
		
		self.doc.insertBefore(layout, textXFormNode)
		
		xForm1D = self.components['XForm1D']
		if not xForm1D:
			raise DomException, "XForm1D not found in components"
		self.doc.insertBefore(xForm1D, layout)
		# now compute and insert XForm1D
		
		# whole-object connections do not need these elements
		killTags = ['XForm', 'Geom']
		
		# print 'Killing %d tags ...' % len(killTags)
		for tag in killTags:
			node = self.selectSingleNode(self.dom, 'Shape/'+tag)
			if not node:
				raise Exception, 'could find node to kill: %s' % tag
			removed = self.doc.removeChild (node)
			removed.unlink()
			# print ' - REMOVED', tag
		
	def addCustomAttrs (self, opts):
		"""
		called in Shape.__init__ just before DOM is updated with
		values from Shape attrs
		"""
		
		# print 'addCustomAttrs: %s' % opts
		
		self.xpaths.update ({
			'EndArrow' : 'Shape/Line/EndArrow'
			})
		
		self.ObjType = 2
		self.EndArrow = 1

		
if __name__ == '__main__':
	line = Line('1')
	print line
