"""
SampleSetManager - reads the standards data file into StandardsGroups,
randomly selecting samples from each group/band. the sample sizes are computed
to generate a "representative" size for each group/band.

The selected samples will be sumbmitted to the SAT service for suggestions for
each of the 5 states.

"""

import sys, os
import math
from UserDict import UserDict
from UserList import UserList
from random import randint, sample

from sat_utils import domain_groups_keys, band_cmp
import sat_utils
from NSESStandardsPool import NSES_stds_pool
from asn import makeFullId, getNumId
from SatServiceClient import SATClient
from SatServiceClient import ResponseError

import codecs
from JloXml import XmlRecord
from JloXml.XmlUtils import createDocument, getChild, getText, getChildText, \
                            addChild, addElement

class SuggestionSet (UserDict):
	"""
	1 SuggestionSet per NSES standard. (There will be about 50 total)
	A SuggestionSet holds the suggestions returned from SAT for the NSES_std.
	
	There are 5 suggestions for each state (state_list holds 5 states).
	The suggestions for each state are represented by a SATServiceRecord.
		- The SATServiceRecords are stored as a UserDict, keyed by state.
	"""
	
	output_dir = "suggestionSets"
	
	def __init__ (self, nses_id, group, band):
		self.nses_id = nses_id
		self.group = group
		self.band = band
		self.state_list = sat_utils.state_list
		self.filename = "%s_%s_%s.xml" % (self.group, self.band, getNumId (self.nses_id))
		UserDict.__init__ (self)

		## print "SuggestionSet - id: %s" % self.nses_id

	def setStateList (self, states):
		"""
		set the list of states for which suggestions are obtained
		"""
		self.state_list = states
		
	def load (self):
		"""
		retrieve the suggested state standards for each state
		"""
		for state in self.state_list:
			try:
				self[state] = self._get_suggestions (state)
			except ResponseError, err:
				print "SAT Service error: " + err
			# except:
				# print "Unknown error: ", sys.exc_info()[0], sys.exc_info()[1]
			
	def _get_suggestions (self, state):
		"""
		obtain suggestions for the specified state via SAT service
		"""
		return  SATClient().doSuggestStandards (self.nses_id, state, self.band)

	def report (self):
		print "NSES: " + self.nses_id
		print "\t group: " + self.group
		print "\t band: " + self.band
		print ""

		for state in self.keys():
			print "\n*** %s ***" % state
			rec = self[state]
			rec.showRequestInfo()
			for std in rec.getSuggestedStandards():
				std.display()
				
	def _toXML (self):
		"""
		Create the XML that is written to the SuggestionSet files.
		
		possible state standard tags are:
			"purlId", "state", "gradeLevels", "text", "benchmark"
		"""
		state_std_tags = ["purlId", "text", "gradeLevels", "benchmark"]
		doc = createDocument (self.__class__.__name__)
		root = doc.documentElement
		info = addElement (doc, root, "SetInfo")
		for tagName in ["nses_id", "group", "band"]:
			addChild (doc, tagName, getattr(self, tagName), info)
		for state in self.keys():
			rec = self[state]
			sel = addElement (doc, root, "Suggestions")
			sel.setAttribute ("state", state)
			for std in rec.getSuggestedStandards():
				sel.appendChild (std.toXML(state_std_tags))
		return doc						 
	
	def writeXML (self, path=None):
		if path is None:
			path = os.path.join (self.output_dir, self.filename)
		f = open(path, 'w')
		f.write (self._toXML().toprettyxml("  "))
		f.close()
		
class SampleSet (UserDict):
	"""
	Represents a CELL of the SAT Eval matrix (axis are group and band). SampleSets
	contain radomly sampled NSES standards lists (the size is computed to be "representational"
	of the percentage of total standards that fall within the particular cell).
	
	For each NSES standard, a SuggestionSet is stored in a dict (keyed by NSES id).
	"""
	
	def __init__ (self, group, band, sample):
		UserDict.__init__ (self)
		self.group = group
		self.band = band
		self.NSES_stds = sample

		## self.report()

		for nses_std in sample:
			nses_id = makeFullId (nses_std)
			sugg_set = SuggestionSet (nses_id, group, band)
			self[nses_std] = sugg_set

	def report (self):
		print "SampleSet - group: %s, band: %s (%d)" % (self.group,
														self.band,
														len (self.NSES_stds))
			
	def getSuggestionSet (self, nses_std):
		return self[nses_std]
		

class SampleSetManager (UserList):
	"""
	- randomly selects standards from each cell of the NSES_stds_pool (SampleSets)
		- NOTE: SampleSets consist of SuggestionSets for each SampleSet member
	"""
	total_stds = 305
	dataset_size = 50

	def __init__ (self):
		self.data = []
		UserList.__init__ (self, self.data)
		self.load ()

	def getSampleSet (self, group, band):
		"""
		select the sampleSet (a set of NSESestandards) having specified
		group and band. NOTE: this corresponds to the standards within a cell of the
		NSES_stds_pool
		"""
		for set in self:
			if set.group == group and set.band == band:
				return set
			
	def getSuggestionSets (self):
		sets = []
		for sampleSet in self:
			# print "sampleSet: %s, %s (%d)" % (sampleSet.group, sampleSet.band, len(sampleSet.NSES_stds))
			for suggestionSet in sampleSet.values():
				# print "\t%s" % suggestionSet.nses_id
				sets.append (suggestionSet)
		return sets
		
	def showSampleSets (self):
		total = 0
		for sampleSet in self:
			total = total + len (sampleSet)
		
		print "SampleSets (%d total stds)" % total
		
		for group in domain_groups_keys:
			print "\n*** %s ***" % group
			for band in ["K-4", "5-8", "9-12"]:
				sampleSet = self.getSampleSet (group, band)
				print "\t%s (%d)" % (sampleSet.band, len(sampleSet.NSES_stds))
				for id in sampleSet.keys():
					print "\t\t%s" % id
				
	def load(self):
		"""
		traverse the NSESStandardsPool map, first by group, then by band
		
		when we get to the (group, band) level we randomly select a sample
		of NSES ids, and from this sample, create a SampleSet.
		
		NOTE: SampleSet instance instantiates a SuggestionSet for each member
		"""
		for group_name in domain_groups_keys:
			# print "\n*** %s ***" % group_name
			group = NSES_stds_pool[group_name]
	
			bands = group.keys()
			bands.sort(band_cmp)
			for band in bands:
				sample = self._get_sample (group[band])	
				# instantiate the SampleSet, which in turn instantiates SuggestionSets
				self.append (SampleSet ( group_name, band, sample))
					
	def _get_sample_size (self, n):
		percent = float (self.dataset_size) / self.total_stds

		# round to nearest int
		size = math.modf (percent * n)
		if (size[0] > .5):
			return int (size[1] + 1)
		else:
			return int (size[1])

	def _get_sample (self, stds):
		"""
		randomly select a sample of computed size from stds list
		"""
		sample_size = self._get_sample_size (len(stds))
		return sample (stds, sample_size)

	def writeSuggestionSets (self):
		sets = self.getSuggestionSets()
		for i in range (len (sets)):
			set = sets[i]
			print "%d/%d %s" % (i, len(sets), set.nses_id)
			set.load()
			set.writeXML()
		
def suggestionSetTester ():
	"""
	get the SAT sugge
	"""
	group = "Applied"
	band = "9-12"
	id = makeFullId ("S101D6D8")
	set = SuggestionSet (id, group, band)
	set.load()
	set.report()

	set.writeXML ()


def sampleSetManagerTester ():

	mgr = SampleSetManager ()
	sampleSet = mgr.getSampleSet ("Subject", "[K-4]")
	if sampleSet:
		sampleSet.report()
	else:
		print "sampleSet not found"
		


def showSampleSets ():
	mgr = SampleSetManager()
	sets = mgr.showSampleSets()
		
if __name__ == "__main__":
	# suggestionSetTester()
	SampleSetManager().writeSuggestionSets()
