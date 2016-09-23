import os, sys
import globals
import massager
from misc.titlecase import titlecase

class CollectionProcessor(massager.CollectionProcessor):
	"""
	calls process on each of the records in the collection
	"""
	
	def process (self, rp):
		# self.showTitles(rp)
		self.showAltTitles(rp)
		
	def showTitles(self, rp):
		title = rp.title
		newtitle = titlecase(title)
		
		if title != newtitle:
			print "\n%s" % rp.recId
			print "\t old: %s" % title
			print "\t new: %s" % newtitle
			
	def showAltTitles(self, rp):
		altTitle = rp.lib_dc_rec.getFieldValue ("library_dc:altTitle");
		if not altTitle: return
		newAltTitle = titlecase(altTitle)
		
		if altTitle != newAltTitle:
			print "\n%s" % rp.recId
			print "\t old: %s" % altTitle
			print "\t new: %s" % newAltTitle
			
def doAll ():
	for collection in globals.collectionNameMap.keys():
		CollectionProcessor (collection)
			
if __name__ == '__main__':
	# CollectionProcessor ("technotes")
	doAll()
