"""
scan the repository by traversing metadata records

/text//concept/relations/relation/id:"NSDL id not found"

"""
import os, sys
from JloXml import XmlUtils
from backpack.object_model.bp_share import repository
from backpack import ConceptsRecord, Relation

concepts_dir = os.path.join (repository, 'concepts')
topics_dir = os.path.join (concepts_dir, 'topics_bp')
chapters_dir = os.path.join (concepts_dir, 'chapters_bp')
units_dir = os.path.join (concepts_dir, 'units_bp')

class AbstractScanner (ConceptsRecord):
	
	base_dir = None
	
	def __init__ (self, id):
		path = os.path.join (self.base_dir, id+'.xml')
		ConceptsRecord.__init__ (self, path=path)

	def getRelationIds (self):
		ids=[];add=ids.append
		for rel in self.relations:
			if rel.id:
				add (rel.id)
		return ids
		
class TopicScanner (AbstractScanner):
	"""
	find the bad links
	"""
	
	base_dir = topics_dir
	
	def __init__ (self, id):
		AbstractScanner.__init__ (self, id)
		self.shortTitle = self.getShortTitle()
		self.badIds = self.getBadIds()
		if 0 and self.badIds:
			print '%d bad ids found for "%s" (%s)' % (len(self.badIds), self.shortTitle, self.getId())
		
	def hasBadIds (self):
		return self.badIds
			
	def getBadIds (self):
		return filter (lambda x:x.startswith("NSDL id not found for"), self.getRelationIds())
		
	def __repr__ (self):
		s=[];add=s.append
		add ('%d bad ids found for "%s" (%s)' % (len(self.badIds), self.shortTitle, self.getId()))
		for badId in self.badIds:
			add ("\t%s" % badId)
		return '\n'.join(s)
		
	def report (self):
		# print "\n%s (%d)" % (self.shortTitle, len(self.badIds))
		print "\n%s" % self.shortTitle
		for badId in self.badIds:
			print ' - %s' %  badId.split()[-1]
				
class ChapterScanner (AbstractScanner):
	
	base_dir = chapters_dir
	
	def __init__ (self, id):
		AbstractScanner.__init__ (self, id)
		self.shortTitle = self.getShortTitle()
		
		self.badTopics = self.getTopicsWithBadIds()
		
	def report (self):
		
		# print '\n%s (%d)' % (self.shortTitle, len(self.badTopics))
		print '\n%s' % self.shortTitle
		for topic in self.badTopics:
			topic.report()
			
		
	def getTopicsWithBadIds(self):
		results=[];add=results.append
		for id in self.getRelationIds():
			topicScanner = TopicScanner(id)
			if topicScanner.hasBadIds():
				add (topicScanner)
		return results
			
class UnitScanner (AbstractScanner):

	base_dir = units_dir	
	
	def __init__ (self, id):
		AbstractScanner.__init__ (self, id)
		self.shortTitle = self.getShortTitle()
		print self.shortTitle
		
		self.badChapters = self.getChaptersWithBadIds()
		
	def getChaptersWithBadIds (self):
		results=[];add=results.append
		for id in self.getRelationIds():
			chapterScanner = ChapterScanner(id)
			if chapterScanner.badTopics:
				add (chapterScanner)
		print 'found %d bad chapters' % len(results)
		return results
		
	def report (self):
		# print '\n-- %s -- (%d)' % (self.shortTitle, len(self.badChapters))
		print '\n-- %s --' % self.shortTitle
		for chapter in self.badChapters:
			chapter.report()
	
def tester():
	if 0:
		id = 'BP-TOPIC-000-000-000-096'
		scanner = TopicScanner (id)
	elif 0:
		id = 'BP-CHAPTER-000-000-000-011'
		scanner = ChapterScanner (id)
	else: 
		id = 'BP-UNIT-000-000-000-003'
		scanner = UnitScanner(id)
		scanner.report()	
		
if __name__ == '__main__':
	for filename in os.listdir(units_dir):
		root, ext = os.path.splitext(filename)
		scanner = UnitScanner(root)
		scanner.report()

