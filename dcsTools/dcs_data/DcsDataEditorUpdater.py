"""

- walkingLastEditorUpdater

	updates editor if the editor listed in the most recent status entry is obsolete. 
"""
import os, string
from nsdlToLdap_Globals import DcsDataRecord  # just to get the DcsDataRecord class defined there
from walkingUpdater import WalkingUpdater, Updater
	
class EditorUpdater (Updater):
	
	DO_WRITES = 0
	
	def __init__ (self, path):
		self.rec = DcsDataRecord (path)
		self.usernameMappings = self.getUsernameMappings()
		self.updateLastEditor()
		self.updateAllEntries()
		# print self.rec
		# print self.rec.getLastEditor()
		if self.DO_WRITES:
			self.rec.write()
			print "wrote ", self.rec.getId()
		else:
			print "WOULD HAVE written", self.rec.getId()
			# print self.rec

	def getUsernameMappings (self):
		"""
		this method must be overridden
		"""
		print "DcsDataEditorUpdater.getUsernameMappings"
		return None
			
	def updateRecentEntry (self):
		entry = self.rec.getCurrentStatusEntry()
		self.updateEntry (entry)
		
	def updateAllEntries (self):
		for entry in self.rec.entryList:
			self.updateEntry (entry)
		
	def updateLastEditor (self):
		lastEditor = self.rec.getLastEditor()
		if self.usernameMappings.has_key (lastEditor):
			newEditor = self.usernameMappings[lastEditor]
			if '?' in newEditor:
				# print 'not setting to ' + newEditor
				return
			if lastEditor != newEditor:
				self.rec.setLastEditor(newEditor)
				# print "switched lastEditor from '%s' to '%s'" % (lastEditor, newEditor)
			
	def updateEntry (self, entry):
		if self.usernameMappings is None:
			raise KeyError, "usernameMappings is not initialzed"
		editor = entry.get("editor")
		# print '\ncurrent editor: "%s"' % editor
		if self.usernameMappings.has_key (editor):
			newEditor = self.usernameMappings[editor]
			if '?' in newEditor:
				# print 'not setting to ' + newEditor
				return
			entry.set ("editor", newEditor)
			if editor != newEditor:
				# print "%s --> %s" % (editor, newEditor)
				# print 'new editor: "%s"' % entry.get ("editor")
				pass
			
class WalkingEditorUpdater (WalkingUpdater):
	"""
	recursively visits an entire directory structure and update all the .xml
	files it finds
	"""
	verbose = 0
	UPDATER_CLASS = EditorUpdater
				
			
def showUsernameMappings(mapping):
	for key in mapping.keys():
		print "%s: %s" % (key, mapping[key])

if __name__ == "__main__":
	# baseDir = os.path.join (UCAS_DIR, 'records/dcs_data')
	##baseDir = os.path.join (UCAS_DIR, 'records/dcs_data/library_dc/theses')
	# WalkingEditorUpdater (baseDir)
	pass
	

	

