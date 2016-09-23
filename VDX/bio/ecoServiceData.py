"""
EcoService Client
"""
import os, sys, time
import demjson
from serviceclient import SimpleClient, SimpleClientError 
# from serviceclient import RequestsClient # future
from UserDict import UserDict
from UserList import UserList
from constants import DATA_SERVICE_URLS

# class EcoServiceClient (RequestsClient): # future
class EcoServiceClient (SimpleClient):
	
	# url to ecoService data service
	default_baseUrl = DATA_SERVICE_URLS['SPRING_15']
	verbose = 0
	
	def __init__ (self, params, baseUrl=None):
		baseUrl = baseUrl or self.default_baseUrl
		# print 'EcoServiceClient'
		# print ' - baseUrl: %s' % baseUrl
		SimpleClient.__init__ (self, baseUrl)
		resp_json = self.getResponseJson(params)

		# print '\n resp KEYS'
		# for key in resp_json:
		# 	print '-', key
		# 	for key2 in resp_json[key]:
		# 		print '  -', key2

		if resp_json.has_key('error'):
			raise Exception, resp_json['error']

		if resp_json['data'].has_key('error'):
			raise Exception, 'DATA error: %s' % resp_json['data']['error']
			
		if not params.has_key('data_type'):
			params['data_type'] = 'data'
			
		if params['data_type'] == 'data':
			self.data = resp_json['payload']['data']
			self.relation = resp_json['payload']['relation']
		
		elif params['data_type'] == 'all':
			self.data = resp_json['data']['payload']['data']
			self.relation = resp_json['data']['payload']['relation']
			self.vocab = resp_json['vocab']['payload']
			self.roster = resp_json['roster']['payload']
			
		if self.verbose:	
			for attr in ['data', 'relation', 'vocab', 'roster']:
				print ' - %s: %d' % (attr, len(getattr(self, attr)))
			
	def getResponseJson (self, params, opts=None):
		"""
		data_type == 'data' returns
		{
			data_version
			payload
				relation
				data
		}
		
		data_type == 'all' returns
		{
		  elapsed_time
		  vocab
		    payload
		  data
			payload
			  relation
			  data
		  roster
		  	payload
		  }
		"""
		respData = self.getData(params, opts)
		# print 'RESPONSE DATA\n%s' % respData
		return demjson.decode(respData)
		
	def filterDataByGroup(self, group):
		raise Exception, "filterDataByGroup not implemented"
		print "filterDataByGroup() - %s" % group
		return self.data
		
		
class Record (UserDict):
	"""
	provides dict api to a row of data
	- casts all values to utf-8 string
	"""
	def __init__ (self, row, schema):
		self.data = {}
		for i, field in enumerate(schema[:len(row)]):
			try:
				self.data[field] = unicode(row[i]).encode('utf-8', 'ignore')
			except Exception, msg:
				print "Record ERROR: %s" % msg
  
class WorkSheet(UserList):
	"""
	Extends CvsFile (sic) to expose:
	- idMap which maps id to record
	"""
	additional_header_rows = 0 # in addition to headers
	key_field = 'id'
	name = "WorkSheet"
	
	def __init__ (self, raw_data):
		# print '%d lines read' % len(raw_data)
		# print 'reading', self.name
		self.headers = raw_data[0]
		self.data = map(lambda x:Record(x,self.headers), raw_data[1+self.additional_header_rows:])
		self.idMap = self._getIdMap()
		
	def _getIdMap (self):
		"""
		calculates idMap, which maps recId to the record
		"""
		# print '_getIdMap looking at %d items' % len(self.data)
		idMap = UserDict()
		for i, rec in enumerate(self.data):
			rec['nodeId'] = str(i+1)
			try:
				idMap[rec[self.key_field]] = rec
			except Exception, msg:
				raise Exception, "could not put record in idMap: %s" % msg
		# print ' ... idMap has %d entries' % len(idMap)
		return idMap
		
	def get (self, id):
		if not self.idMap.has_key(id):
			return None
		return self.idMap[id]
		
	def update(self, data):
		"""
		just data not headers
		"""
		self.data = data
		self.idMap = self._getIdMap();
		
class RelationTable (WorkSheet):
	"""
	Specialized WorkSheet for the relation worksheet
	"""
	additional_header_rows = 0
	name = "RelationTable"
	
class RosterTable (WorkSheet):
	"""
	Specialized WorkSheet for the relation worksheet
	"""
	additional_header_rows = 0
	key_field = 'Email'
	name = "RosterTable"
	
	def getGroup(email):
		rec = self.get(email)
		if not rec:
			return None
		return rec['Email']
		
	
		
class DataTable (WorkSheet):
	additional_header_rows = 3
	name = "DataTable"
	
	def __init__ (self, raw_data):
		WorkSheet.__init__(self, raw_data)
		self.nodeMap = self._getNodeMap();
	
	def _getNodeMap (self):
		"""
		add another field to the schema ('nodeId')
		and make a map from nodeId to the record
		"""
		self.headers.append('nodeId')
		nodeMap = UserDict()
		for i, rec in enumerate(self.data):
			rec['nodeId'] = str(i+1)
			# print ' - nodeId: %s' % rec['nodeId']
			nodeMap[rec['nodeId']] = rec
		return nodeMap	
		
	def getNameFromId(self, id):
		if not self.idMap.has_key(id):
			# print "WARN: rec not found for %s" % id
			return None
		return self.idMap[id]['Name']
	
	def getName(self, id):
		rec = self.get(id)
		if not rec:
			# print 'rec not found for %s' % id
			return None
		return rec['Name']
		
	def getNodeId(self, id):
		rec = self.get(id)
		if not rec:
			# print 'rec not found for %s' % id
			return None
		return rec['nodeId']
		
class RecReferenceError (Exception):
	pass

		
class GraphData:
	"""
	calculates edge_data using data from the 'data' and 'relation' worksheets
	"""
	def __init__(self, params, baseUrl=None):
		client = EcoServiceClient(params, baseUrl)
		self.baseUrl = client.baseUrl # get it from source
		self.relation_table = RelationTable(client.relation)
		self.data_table = DataTable(client.data)
		self.roster_table = RosterTable(client.roster)
		
		# print 'before: %d relations' % len(self.relation_table)
		
		if params.has_key('group'): 
			relation_data = self.filterRelationsByGroup(params['group'])
			self.relation_table.update(relation_data)
		
		# print 'after: %d relations' % len(self.relation_table)
			
	def filterRelationsByGroup(self, group):
		# print ' filterRelationsByGroup - %s (%s)' % (group, type(group))
		def accept (relation_rec):
			for attr in ['Subject', 'Object']:
				try:
					id = relation_rec[attr]
					data_rec = self.data_table.get(id)
					
					if not data_rec:
						raise RecReferenceError, 'data_rec not found for %s' % id
						
					if self.baseUrl == DATA_SERVICE_URLS['SPRING_15']: # this is pre-rec-groups (which we'll have to support?)
						email = data_rec.get('Creator')
						roster_rec = self.roster_table.get(email)
						if not roster_rec:
							raise RecReferenceError, 'roster_rec not found for %s' % email
						roster_rec_group = roster_rec.get('Group')
						# print 'id: %s, group: %s' % (id, roster_rec_group)
						if roster_rec_group != group:
							return 0
							
					elif self.baseUrl == DATA_SERVICE_URLS['FALL_15']:# using rec_group
						return data_rec.get('Group') == group
						
					else:
						raise Exception, "self.baseUrl not recognized (%s)" % self.baseUrl
						
				except RecReferenceError, msg:
					# print "WARN: %s" % msg
					return 0
			# print 'ACCEPTED relation %s' % relation_rec.get('id')
			return 1
			
		accepted = []
		for reln_rec in self.relation_table.data:
			if accept(reln_rec):
				accepted.append(reln_rec)
		return accepted
		# return filter (accept, self.relation_table.data)
	
	def getEdgeData (self):
		"""
		returns a list of Edges, which have attributes:
		- source
		- relation
		- target
		- data (which is used by layout to position and
		        decorate edges)
		"""
		# try to accomadate relation objects that are not
		# nodes (e.g., abiotic factors). 
		#  --- Never tested. Not currently used. ---
		extra_id_counter = 900
		if 0:
			idMap = self.data_table.idMap
			for key in idMap.keys():
				# print '- %s: %s' % (key, idMap[key])
				print '- %s: %s' % (key, idMap[key]['Name'])
				
		edgeData = []
		for i, rec in enumerate(self.relation_table.data):
			
			subjectId = rec['Subject']
			subjectNodeId = self.data_table.getNodeId(subjectId);
			if not subjectNodeId:
				print "WARN: subject record not found for " + subjectId
				continue
			subjectName = self.data_table.getName(subjectId);
			objectId = rec['Object']
			objectNodeId = self.data_table.getNodeId(objectId);
			if not objectNodeId:
				# couldnt find a record for this id - treat it like a abiotic
				objectName = objectId
				objectNodeId = str(extra_id_counter)
				extra_id_counter = extra_id_counter + 1
			else:
				objectName = self.data_table.getName(objectId)
			
			# EDGE_DATA_STRUCTURE
			this_edge_data = {
				'source':subjectId,
				'relation': rec['Relation'],
				'target':objectId,
				'data': {
					'sourceId':subjectId,
					'sourceLabel':subjectName,
					'sourceNodeId':subjectNodeId,
					'targetId':objectId,
					'targetLabel':objectName,
					'targetNodeId':subjectNodeId
				}
			}
			edgeData.append(this_edge_data)
		return edgeData

def getEcoServiceGraphData (params=None, baseUrl=None):
	"""
	Static method returning graphData
	"""
	_params = {
		# 'section' : 'Period 1',
		# 'teacher' : 'holly',
		# 'group' : '2',
		'command' : 'data',
		'data_type' : 'all',

	}
	# params = params or _params
	if params:
		_params.update(params)
	return GraphData(_params, baseUrl)

def dataTableTesters (params):
	client = EcoServiceClient(params, baseUrl)
	data_table = DataTable(client.data)
	
	if 1:
		print "idMap"
		for rec in data_table.idMap.values():
			print '- %s - %s (%s)' % (rec['nodeId'], rec['id'], rec['Name'])

	if 2:
		print "nodeMap"
		for key in data_table.nodeMap.keys():
			print '- %s : %s' % (key, data_table.nodeMap[key])

	if 1:
		print '%d records in data_table' % len (data_table)
		for rec in data_table:
			print '- %s - %s (%s)' % (rec['nodeId'], rec['id'], rec['Name'])

def relationTableTesters(params):
	client = EcoServiceClient(params, baseUrl)
	relation_table = RelationTable(client.relation)
	data_table = DataTable(client.data)
	print '%d records in relation_table' % len (relation_table)
	print relation_table.headers
	for rec in relation_table:
		# print rec
		# continue
		subjectId = rec['Subject']
		subjectName = data_table.getName(subjectId)
		objectId = rec['Object']
		objectName = data_table.getName(objectId) or objectId
		print '- %s (%s) -> %s -> %s (%s)' % (subjectName, rec['Subject'], 
			rec['Relation'], objectName, objectId)

def clientTester (params):
	client = EcoServiceClient(params, baseUrl)
	print 'data has %d rows' % len (client.data)
	print 'relation has %d rows' % len (client.relation)
	
	dataWS = DataTable(client.data)
	for id in dataWS.idMap.keys():
		print ' - ',id
		
if __name__ == '__main__':		
	# teacher, section, group = 'dls', 'CCS-Dev-Mtg', '2'
	if 0:
		teacher, section, group = 'crump', 'Period 3', '1' # works with SPRING_15
		baseUrl_name = 'SPRING_15'
	elif 0:
		teacher, section, group = 'crump', 'Period 3', '2' # works with 
		baseUrl_name = 'FALL_15'
	else:
		teacher, section, group = 'brown', 'Periods 4 and 7', '1' # works with
		baseUrl_name = 'FALL_15'

	params = {
		'section' : section,
		'teacher' : teacher,
		'group' : group,
		'command' : 'data',
		'data_type' : 'all',
		'force' : 'true'
	}
	# dataTableTesters(params)
	# relationTableTesters(params)
	print '------------'

	print 'baseUrl_name: %s' % baseUrl_name
	for p in params:
		print ' - %s: %s' % (p, params[p])
	baseUrl = DATA_SERVICE_URLS[baseUrl_name]
	graphData = GraphData(params, baseUrl)
	edgeData = graphData.getEdgeData()
	if 0:
		for edge in edgeData:
			print " - %s" % (edge)
	print "%d Edges computed" % len(edgeData)
	if 0:
		from JloGraph import Layout
		layout = Layout(edgeData)
		print 'Layout: %s' % layout

