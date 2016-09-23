import os, sys
from PubNameXSD import PubNameXSD
from InstNameXSD import InstNameXSD

class VocabBlender:
	"""
	assume schemas to be blended live in same directory
	"""
	schemadir = "/home/ostwald/Documents/NCAR Library/Citations project/schemaBlending"
	xsdClass = None
	
	def __init__ (self, filename1, filename2):
		self.filename1 = filename1
		self.filename2 = filename2
		self.dups = []
		
		self.vocabTerms = self.getVocabTerms (filename1)
		for term in self.getVocabTerms (filename2):
			if not term in self.vocabTerms:
				self.vocabTerms.append (term)
			else:
				self.dups.append (term)
		
		self.vocabTerms.sort(lambda x,y:cmp (x.lower(), y.lower()))
				
	def getVocabTerms (self, filename):
		xsdpath = os.path.join (self.schemadir, filename)
		# xsd = PubNameXSD (path=xsdpath)
		xsd = self.xsdClass (path=xsdpath)
		self.xsdTemplate = xsd
		return self.getVocabFn (xsd)
		
	def write (self, filename):
		if filename == self.filename1 or filename == self.filename2:
			raise Exception, 'cant write to existing vocab schema!'
		self.setVocabFn (self.xsdTemplate, self.vocabTerms)
		self.xsdTemplate.write (os.path.join (self.schemadir, filename))
		
class PubNamesBlender(VocabBlender):
	xsdClass = PubNameXSD
	getVocabFn = PubNameXSD.getPubNames
	setVocabFn = PubNameXSD.setPubNames
	
class InstNamesBlender(VocabBlender):
	xsdClass = InstNameXSD
	getVocabFn = InstNameXSD.getInstNames
	setVocabFn = InstNameXSD.setInstNames
			
def doPubNamesBlend ():
	xsd1 = 'WOS-pubNames.xsd'
	xsd2 = 'PUBS-pubnames.xsd'
	blender = PubNamesBlender (xsd1, xsd2)
	print '%d terms' % len (blender.vocabTerms)
	print '%d pubs pubnames' % len (blender.dups)
	blender.write('unionPubNames3.xsd')
	
def doInstNamesBlend ():
	xsd1 = 'instName-from-libraryDC.xsd'
	xsd2 = 'instName-from-PUBS-publisher.xsd'
	blender = InstNamesBlender (xsd1, xsd2)
	print '%d terms' % len (blender.vocabTerms)
	print '%d dups' % len (blender.dups)
	blender.write('unionInstNames.xsd')
	
if __name__ == '__main__':
	doInstNamesBlend ()
	
