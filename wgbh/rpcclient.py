"""
SEE http://www.teachersdomain.org/tdwiki/doku.php/partner:the_teachers_domain_educational_standards_api#the_teachers_domain_lexicon
"""
import sys
import xmlrpclib

def encode(s):
	errors = 'xmlcharrefreplace' # ignore replace xmlcharrefreplace strict backslashreplace
	# return s.encode ('utf8', errors )
	return s.encode ('ascii', errors )

class XML_RPC_Client:

	href = None # abstract

	def __init__ (self):
		self.server = xmlrpclib.ServerProxy(self.href)

	def listMethods (self):
		return self.server.system.listMethods()
		
class WGBH_Client(XML_RPC_Client):

	"""
	This class wraps the Teachers Domain API calls
	"""
	
	href = "http://standards.teachersdomain.org/td_standards_rpc/"
	verbose = 1

	def __init__ (self):
		XML_RPC_Client.__init__ (self)
		if not self.alive():
			raise Exception, "server is not alive"

	def alive (self):
		return self.server.alive()

	def getErrorMsg (self, code):
		codes = self.get_error_codes()
		print "codes is a %s" % type(codes)
		print "code is a %s" % type(code)
		return codes[code]
		
	def getResponse (self, data):
		if data[0] != 200:
			error_code = data[0]
			error_msg = self.getErrorMsg(error_code)
			print "error_msg: %s" % error_msg
			raise Exception, "Error: %s (%s)" % (error_code, error_msg)
		return data[1]

	def get_error_codes (self):
		# return self.getResponse (self.server.get_error_codes())
		
		try:
			response = self.getResponse(self.server.get_error_codes())
		except:
			raise Exception, "get_error_codes error: %s" % sys.exc_info()[1]
			
		# the response is a string (that looks like a dict) ...
		code_data = response[1:-1]
		code_dict = {}
		for mapping in code_data.split(","):
			x = mapping.find(':')
			code = int(mapping[:x].strip())
			msg = mapping[x+1:].strip()
			if msg[0] in ['"',"'"] and msg[0] == msg[-1]:
				msg = msg[1:-1]
			code_dict[code] = msg
			
		if self.verbose:
			print code_dict
			
		return code_dict
		
	def get_term_catalogue_with_id (self):
		"""
		Returns a list of all lexicon terms and thier IDs: e.g., 
			['Government :: Constitution', 6898]
			[' Writing :: Purpose:: Recording/Reporting', 5605]
			['advanced physics :: quantum mechanics', 755]
			['advanced physics :: relativity', 888]
				...
				
		NOTES:
			1 - the lexicon terms are not represented uniformily wrp white spaces, so
				after splitting on "::" we must trim the values
			2 - the items in the list returned by this function have the form:
				[ lexicon_entry, id]
		"""
		
		response = self.getResponse(self.server.get_term_catalogue_with_id ())
		if self.verbose:
			response.sort(lambda a,b: cmp(a[0].lower(), b[0].lower()))
			for pair in response:
				print "%s (%s)" % (pair[0], pair[1])
				
		return response
		
	def get_jurisdiction_list(self):
		"""
		Returns a complete list of Jurisdictions arranged in Code/Name pairs
		"""
		try:
			response = self.getResponse(self.server.get_jurisdiction_list())
		except:
			raise Exception, "get_jurisdiction_list error: %s" % sys.exc_info()[1]
		
		if self.verbose:
			print '\n** get_jurisdiction_list **'
			for item in response:
				print "\t%s  %s" % (encode(item[0]), encode(item[1]))
		
		return response

	def crosswalk_asn_to_jurisdiction (self, ASN_id, jurisdiction, grade_range=None):
		"""
		Crosswalking one ASN Statement ID to comparable ID associated with an alternate Jurisdiction
		
		jurisdiction is required
		grade_range is required
		
		use example:
			crosswalk_asn_to_jurisdiction('S100FE86','NY','K-12')
		return example: 
			['S102742A', 'S1027608']
		"""
		grade_range = grade_range or 'k-12'
		
		try:
			response = self.getResponse(self.server.crosswalk_asn_to_jurisdiction (ASN_id, jurisdiction, grade_range))
		except:
			raise Exception, "crosswalk_asn_to_jurisdiction error: %s" % sys.exc_info()[1]
			
		if self.verbose:
			print '\n** crosswalk_asn_to_jurisdiction (%s, %s, %s) **' % (ASN_id, jurisdiction, grade_range)
			print response
		
		return response
		
	def get_lexicon_term_for_ASN_statement_ID(self, ASN_id):
		"""
		Return a list of Lexcion Term IDs correlated to the supplied ASN Statement ID
		use example:
			get_lexicon_term_for_ASN_statement_ID('S103DE11')
		return example: 
			[1170, 1609, 1350]
		"""
		try:
			response = self.getResponse(self.server.get_lexicon_term_for_ASN_statement_ID(ASN_id))
		except:
			raise Exception, "get_lexicon_term_for_ASN_statement_ID error: %s" % sys.exc_info()[1]			
		
		if self.verbose:
			print '\n** get_lexicon_term_for_ASN_statement_ID (%s) **' % (ASN_id)
			print '\t', response
		
		return response
		
	def lexicon_to_asn_id (self, jurisdiction, grade_range, lexicon_term):
		"""
		jurisdiction is required
		grade_range is required
		
		The Lexicon Term parameter is an Integer ID for the Lexicon Term. See get_term_catalogue_with_id
  
		Returns list of ASN id and description pairs correlated to the given lexicon term, education level and source.
		use example: lexicon_to_asn_id('NY','k-12',121)
		return example: 
			[['S1027420', '2.1b Each gene carries a single unit of information. ....]]

		"""
		try:
			response = self.getResponse(self.server.lexicon_to_asn_id (jurisdiction, grade_range, lexicon_term))
		except:
			raise Exception, "lexicon_to_asn_id error: %s" % sys.exc_info()[1]
		if self.verbose:
			print '\n** lexicon_to_asn_id (%s, %s, %s) **' % (jurisdiction, grade_range, lexicon_term)
			for item in response:
				print "\n(%s)  %s" % (encode(item[0]), encode(item[1]))
		return response
		
	def get_ASN_statement_ID_for_lexicon_term (self, term, jursidiction=""):
		"""
		Returns a list of ASN statements correlated to the supplied Lexicon Term ID.
		The optional second parameter (jurisdiction) will filter results for the supplied jursidiction code.
		use example:
			get_ASN_statement_ID_for_lexicon_term(1609)
		return example: 
			['S1020678', 'S103DE11', 'S103DEC7', 'S103DF1A']
		"""
		try:
			response =  self.getResponse(self.server.get_ASN_statement_ID_for_lexicon_term (term, jursidiction))
		except:
			raise Exception, "get_ASN_statement_ID_for_lexicon_term error: %s" % sys.exc_info()[1]

		if self.verbose:
			print '\n** get_ASN_statement_ID_for_lexicon_term (%s, %s) **' % (term, jursidiction)
			print "\t", response
		
		return response

	def get_standards_hierarchical_json (self, jurisdiction, terms, grade_range='k-12'):
		
		try:
			response = self.getResponse (
				self.server.get_standards_hierarchical_json (jurisdiction, terms, grade_range))
		except:
			raise Exception, "get_standards_hierarchical_json error: %s" % sys.exc_info()[1]
			
		if self.verbose:
			print '\n** get_standards_hierarchical_json (%s, %s, %s) **' % (jurisdiction, terms, grade_range)
			from std import StdTree
			for tree in response:
				jurisdiction = tree[0]
				data = tree[1]
				tree = StdTree (data, jurisdiction)
				tree.report()
		
		return response		
		
if __name__ == '__main__':
	client = WGBH_Client()
	# client.get_jurisdiction_list ()
	# client.get_term_catalogue_with_id ()
	# client.crosswalk_asn_to_jurisdiction ('S1027420','CO', '7')
	# client.get_lexicon_term_for_ASN_statement_ID ('S103ECA0')
	# client.lexicon_to_asn_id ('NY', 'k-12', '121')
	client.get_ASN_statement_ID_for_lexicon_term (121, 'NY')
	# client.get_standards_hierarchical_json ('NY','121,122','k-12')
	# codes = client.get_error_codes()

