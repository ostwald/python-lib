"""
Class encapsulating log information for a single request
"""

import string, time
import re
import sys
from UserDict import UserDict
from utils import timestamp_fmt, secsToLogTime

log_entry = """
Aug 12, 2005 6:10:11 AM org.apache.struts.action.RequestProcessor process
INFO: Processing a 'GET' for path '/admin/browse'
SessionRegistry: registered sessionBean: 3F657B48A1FD3152A5736D3D00147E68
Aug 12, 2005 6:10:11 AM MDT DCS RequestProcessor: 
	role:  schemedit_admin
	remoteAddr:  209.48.222.162
	URL:  http://dcs.dlese.org/dcc/admin/browse.do
	QueryString:  null
	SessionId:  3F657B48A1FD3152A5736D3D00147E68
SchemEditUtils: Filtered Request Parameters
WorkFlowServices: received a statusEvent!
WorkFlowServices: id: DLESE-000-000-000-888 
WorkFlowServices: collection: dcc 
WorkFlowServices: xmlFormat: adn
WorkFlowServices: current status_|-final-dcc-|_
WorkFlowServices: prior status: _|-final-dcc-|_
"""

class Request:

	def __init__ (self, log_entry):
		self.log_entry = string.strip (log_entry)
		self.sessionId = self.get_field ("SessionId")
		self.command = self.get_field ("command")
		self.time_stamp = self.get_time_stamp()
		self.log_time = secsToLogTime (self.time_stamp)
		self.work_flow_info = self.get_workflow_info()

	def isStatusEvent (self):
		return (hasattr (self, "work_flow_info") and self.work_flow_info is not None)

	def get_workflow_info (self):
		statusEventPat = re.compile ("\nWorkFlowServices: received a statusEvent!")
		m = re.compile (statusEventPat).search (self.log_entry)
		if m:
			return WorkFlowInfo (self.log_entry)

	def get_time_stamp (self):
		log_time_fmt = "[a-zA-Z]*? [\d]*?, [\d]{4} [\d]{1,2}:[\d]{2}:[\d]{2} [A-Z]{2}"
		log_time_pat = re.compile (log_time_fmt)
		
		line1 = self.log_entry.split ("\n")[0]
		# print "line1: *%s*" % line1
		m = log_time_pat.match (line1)
		if m:
			# print "match: ", m.group()
			try:
				time_tuple = time.strptime (m.group(), timestamp_fmt)
				return time.mktime(time_tuple)
			except:
				print sys.exc_info

		# if we get here there has been a parsing error
		print "Request.TimeStampError", "Could not parse: %s" % (line1)

	def get_field (self, field):
		if hasattr (self, field):
			return getattr (self, field)
		pat = "\n\t%s:[ ]+?(.*?)\n" % field
		m = re.compile (pat).search (self.log_entry)
		if m:
			return m.group(1)
		else:
			## print "\n%s not found in \n%s" % (field, self.log_entry)
			if self.isStatusEvent() and self.work_flow_info.has_key (field):
				return self.work_flow_info[field]

	def sampleDisplayMe (self):
		if not self.isStatusEvent():
			return ""
		return self.work_flow_info['id']

	def __repr__ (self):
		s = [];add=s.append
##		add( '_'*20)
##		add( 'timestamp: %s' %  self.time_stamp)
		add( secsToLogTime (self.time_stamp))
		add( 'sessionId: %s' %  self.sessionId)
		add( 'command: %s' %  self.command)
		add( 'remoteAddr: %s' % self.get_field ('remoteAddr'))
		add( 'role: %s' % self.get_field ('role'))
		add( 'lastEditor: %s' % self.get_field ('lastEditor'))
		add( 'status event: %s' %  self.isStatusEvent())
		if self.isStatusEvent():
			add (str(self.work_flow_info))
		return string.join (s, "\n")
	
class WorkFlowInfo (UserDict):

	# define set of import keys and provide a consistent ordering for display
	key_keys = ("id", "collection", "xmlFormat", "prior status", "current status")

	def __init__ (self, log_entry):
		UserDict.__init__ (self)
		self._read_attributes (log_entry)

	def _read_attributes (self, log_entry):
		"""
		extract WorkFlowInfo attributes from the log_entry, and update the dict
		"""

		# regex to extract "normally formatted attributes"
		infoRE = "WorkFlowServices:[ \t]?(?P<attr>.*?):[ \t]+?(?P<val>.*)"

		# kludge for attributes that didn't include a " :" separator for current status
		currentStatusRE = "WorkFlowServices:[ \t]?(?P<attr2>current status)(?P<val2>.*)"

		pat = re.compile ("%s|%s" % (infoRE, currentStatusRE))
		for line in string.split (log_entry, '\n'):
			m = pat.match (line)
			attr = val = ""
			if m:
				g_dict = m.groupdict()
				for key in g_dict.keys():
					if g_dict[key] is not None and key[:3] == 'val':
						val = g_dict[key]
					if g_dict[key] is not None and key[:4] == 'attr':
						attr = g_dict[key]
				if attr and key:
					# print ("adding %s: %s" % (attr, val))
					self[attr]=val

	def __repr__ (self, indent=""):
		"""
		show the WorkFlowInfo attributes
		   first list the "key_keys", then
		   list any other keys
	    """
		s=[];add=s.append
		add ("%sWorkFlowInfo" % indent)
		for key in self.key_keys:
			if self.has_key (key):
				add ("%s: %s" % (key, self[key]))		
		for key in self.keys():
			if not key in self.key_keys:
				add ("%s: %s" % (key, self[key]))
		return string.join (s, "\n\t"+indent)

if __name__ == "__main__":
	r = Request (log_entry)
	print r.get_field("log_time")
	# print WorkFlowInfo (log_entry)
	## print "remoteAdder: %s" % r.get_field("remoteAddr")
	## print "URL: %s" % r.get_field("URL")


	# convert_time ("Aug 12, 2005 2:48:05 AM")

