"""
TreeCensusData Provider (for layout)

data providers from CSV files

provides edgeData and other services for layout

"""

from tabdelimited import CsvRecord
from tabdelimited import CsvFile
from UserDict import UserDict
from VDX import util



class WorkSheet (CsvFile):
	"""
	Extends CvsFile (sic) to expose:
	- idMap which maps id to record
	"""
	linesep = '\r'
	encoding = 'ISO-8859-1' # utf-8
	additional_header_rows = 0 # in addition to headers
	default_file = None # overridden by subclasses
	
	def __init__ (self, file=None):
		file = file or self.default_file
		CsvFile.__init__(self, file)
		self.read (file)
		print '%d lines read' % len(self.data)
		self.idMap = self._getIdMap();
		
	def accept (self, item):
		return item['id'] 
		
	def preprocess (self, filecontents):
		filecontests = CsvFile.preprocess(self,filecontents)
		new = [];add=new.append
		for i, line in enumerate(filecontents.split(self.linesep)):
			# print i
			if len(line.strip()) ==0 or i>0 and i<self.additional_header_rows:
				# print ".. skipped line %d" % i
				continue
				
			add (line);
		print 'about to join %s lines' % len(new)
		return self.linesep.join(new)
			
		
	def _getIdMap (self):
		"""
		calculates idMap, which maps recId to the record
		"""
		print '_getIdMap looking at %d items' % len(self.data)
		idMap = UserDict()
		for i, rec in enumerate(self.data):
			rec['nodeId'] = i
			idMap[rec['id']] = rec
		print ' ... idMap has %d entries' % len(idMap)
		return idMap
		
	def get (self, id):
		if not self.idMap.has_key(id):
			return None
		return self.idMap[id]

class DataTable (WorkSheet):
	"""
	Extends WorkSheet to provide functionality specific to the 'data'
	worksheet, which contains the organism card data
	
	"""
	linesep = '\r'
	additional_header_rows = 3
	default_file = util.getCsvData('Data Sheet')
	
	def __init__ (self, file=None):
		WorkSheet.__init__(self, file)
		self.nodeMap = self._getNodeMap();
		
	def _getNodeMap (self):
		"""
		add another field to the schema ('nodeId')
		and make a map from nodeId to the record
		"""
		self.schema.append('nodeId')
		print '_getNodeMap looking at %d items' % len(self.data)
		nodeMap = UserDict()
		for i, rec in enumerate(self.data):
			rec['nodeId'] = str(i+1)
			# print ' - nodeId: %s' % rec['nodeId']
			nodeMap[rec['nodeId']] = rec
		print ' ... nodeMap has %d entries' % len(nodeMap)
		return nodeMap		
	
	def getNameFromId(self, id):
		if not self.idMap.has_key(id):
			print "WARN: rec not found for %s" % id
		return self.idMap[id]['Name']
	
	def getName(self, id):
		rec = self.get(id)
		if not rec:
			print 'rec not found for %s' % id
			return None
		return rec['Name']
		
	def getNodeId(self, id):
		rec = self.get(id)
		if not rec:
			print 'rec not found for %s' % id
			return None
		return rec['nodeId']
	
class RelationTable (WorkSheet):
	"""
	Specialized WorkSheet for the relation worksheet
	"""
	additional_header_rows = 0
	default_file = util.getCsvData('relation')

class GraphData:
	"""
	calculates edge_data using data from the 'data' and 'relation' worksheets
	"""
	def __init__(self):
		self.relation_table = RelationTable()
		self.data_table = DataTable()
	
	def getEdgeData (self):

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
			
			print ' - ', i, rec['Relation']
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

def dataTableTesters ():
	# filename = 'one-record-tester.csv'
	file = util.getCsvData('Data Sheet')
	data_table = DataTable(file)
	
	if 1:
		print "idMap"
		for rec in data_table.idMap.values():
			print '- %s - %s (%s)' % (rec['nodeId'], rec['id'], rec['Name'])

	if 0:
		print "nodeMap"
		for key in data_table.nodeMap.keys():
			print '- %s : %s' % (key, data_table.nodeMap[key])


	if 1:
		print '%d records in data_table' % len (data_table)
		for rec in data_table:
			print '- %s - %s (%s)' % (rec['nodeId'], rec['id'], rec['Name'])

def relationTableTesters():
	relation_table = RelationTable()
	data_table = DataTable()
	print '%d records in relation_table' % len (relation_table)
	print relation_table.schema
	for rec in relation_table:
		# print rec
		# continue
		subjectId = rec['Subject']
		subjectName = data_table.getName(subjectId)
		objectId = rec['Object']
		objectName = data_table.getName(objectId) or objectId
		print '- %s (%s) -> %s -> %s (%s)' % (subjectName, rec['Subject'], 
			rec['Relation'], objectName, objectId)

if __name__ == '__main__':
	if 0:
		from JloGraph import Layout
		edgeData = GraphData().getEdgeData()
		layout = Layout(edgeData)
		print layout
		
	
		
