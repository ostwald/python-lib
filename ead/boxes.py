import sys,os
from EadRecord import EadRecord

## def getBoxes (collection):

def foo (ead):
	best = ead.getCollection ("ref59")
	best.report()
	

	box = best.getBox("4")
	
	for folder_key in box.keys():
		print "FOLDER: ", folder_key
		folder = box[folder_key]
	
		for item in folder.getItems():
			item.report()
	
def makeLine (box, folder, series, description, notes):
	return "%8s %8s %20s %40s %10s" % (box, folder, series, description, notes)
			
def boxReport (box_key):
	box = best.getBox (box_key)
	s=[];add=s.append
	add (makeLine ('Box', 'Folder', 'Series', 'Description', 'Notes'))
	for folder_key in box.keys():
		folder = box[folder_key]
		add (makeLine (box_key, folder_key, "", "", ""))
	return '\n'.join (s)
	
			
if __name__ == "__main__":
	path = "Final Washington EAD.xml"
	ead = EadRecord (path=path)
	best = ead.getCollection ("ref59")
	best.report()
	
	box_key = "4"
	print boxReport (box_key)
