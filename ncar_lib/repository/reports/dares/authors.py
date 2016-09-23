"""
from Jamica (*'s are mine):
	
Authors can be divided into three categories: those that solely work with DAReS,
collaborators across other NCAR divisions, and a few whose names might cause
some problems. I'll address each individually.

DAReS Authors Can we search across the DCS for *all records* associated with each
of the DAReS authors, identify which collection they're in, determine their
status, and *apply the correct affiliation and people DB identifier*? These
authors include Tim Hoar, Nancy Collins, David Dowell, Glen Romine, and Kevin
Raeder.

NCAR Collaborators These include Chris Snyder (MMM), Joe Tribbia (CGD), Doug
Nychka (IMAGe), and Josh Hacker (RAP). I'm currently not certain about the best
way to catalog these, as it would be inaccurate to designate an affiliation of
DAReS if these individuals do not have official joint appointments. So, let's
hold off on them until I hear back from Tim.

Problem names These include Hui Liu, Jeffrey Anderson, and Nancy Collins. What
I'd like to do for them is generate a list of possible pubs (searching over all
records, using last name and first initial), and then share the lists with each
individual, asking them to confirm or deny each record. Does that sound like a
reasonable approach? A helpful tip for Hui Liu is that he has no middle initial.

"""

# from ncar_lib.par import ParAuthor

from ncar_lib.repository.author_search import Author

class DaresAuthors:
	
	"""
	Author factory - using explicitly defined lists of author data specific
	to the Dares organization
	"""
	
	def getAuthorEntry (self, fullName, authList=None):
		"""
		author entry is a dict(keyed by author fullname) with two values:
			- author (an ncar_lib.repository.author_search.Author instance)
			- instDiv (a string representing an instDiv (e.g., 'DARes')
		"""
		if authList:
			try:
				return getattr (self, authList)[fullName]
			except:
				raise Exception, "'%s' not found in '%s' list" % (fullName, authList)
		else:
			for listName in ['dares_authors', 'ncar_collaborators', 'problem_names']:
				try:
					return self.getAuthorEntry (fullName, listName)
				except:
					pass
			raise Exception, "'%s' not found on any author list" % fullName
			
	def getAuthor (self, fullName, authList=None):
		"""
		returns the ncar_lib.repository.author_search.Author instance for provided
		full name
		"""
		entry = self.getAuthorEntry (fullName, authList)
		return entry["author"]
			
	def getInstDiv (self, fullName, authList=None):
		return self.getAuthorEntry (fullName, authList)["instDiv"]
	
	dares_authors = {
		'Tim Hoar' : {
			'author' : Author('Hoar', 'Tim', upid='11341'),
			'instDiv' : 'DAReS '
			},
		'Nancy Collins' : {
			'author' : Author('Collins', 'Nancy', upid='11218'),
			'instDiv' : 'DAReS '
			},		
		'David Dowell' : {
			'author' : Author('Dowell', 'David', upid='11025'), # David Dowell
			'instDiv' : 'DAReS '
			},
		'Glen Romine' : {
			'author' : Author('Romine', 'Glen', upid='16205'), # Glen Romine
			'instDiv' : 'DARes'
			},
		'Kevin Raeder' : {
			'author' : Author('Raeder', 'Kevin', upid='11342'), # Kevin Raeder
			'instDiv' : 'DAReS'
			}
		}
		
	ncar_collaborators = {
		'Chris Snyder' : { #  (MMM)
			'author' : Author('Snyder', 'Chris', upid='9671'),
			'instDiv' : 'MMM'
			},
		'Joe Tribbia' : { #  (CGD)
			'author' : Author('Tribbia', 'Joe', upid='11904'),
			'instDiv' : 'GCD'
			},
		'Doug Nychka' : { #  (IMAGe)
			'author' : Author('Nychka', 'Doug', upid='444'),
			'instDiv' : 'IMAGe'
			},		
		'Josh Hacker' : { # Josh Hacker (RAP)
			'author' : Author('Hacker', 'Josh', upid=''), # NOT FOUND!
			'instDiv' : 'RAP'
			}
		}

	# NOTE: Nancy Collins is already on dares_authors list
	problem_names = {
		'Hui Liu' : { # 
			'author' : Author('Liu', 'Hui', upid='3350'),
			'instDiv' : 'DARes'
			},
		'Jeffrey Anderson' : { # 
			'author' : Author('Anderson', 'Jeffrey', upid='11641'),
			'instDiv' : 'DARes'
			}
		}
		
def getAllAuthors ():
	daresAuthors = DaresAuthors()
	all_authors=[];add=all_authors.append
	for author_map in [daresAuthors.dares_authors, daresAuthors.ncar_collaborators, daresAuthors.problem_names]:
		for fullName in author_map.keys():
			add (fullName)
	return all_authors
			
		
def getAuthor (fullName):
	return DaresAuthors().getAuthor(fullName)

def getAuthorEntry (fullName):
	return DaresAuthors().getAuthorEntry(fullName)
		
if __name__ == '__main__':
	authors = DaresAuthors()
	name = 'Hui Liu'
	entry = authors.getAuthor(name)
	if name:
		print "entry found for", name
		
	author = authors.getAuthor (name)
	if author:
		print 'author found for %s (%s)' % (name, author.__class__.__name__)

