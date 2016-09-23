"""
Curriculum
"""
import os, sys
import bp_share

from backpack import ConceptsRecord, Relation
from backpack.object_model import *
from backpack.data_model import utils, UnitData
from backpack.data_model.utils import ingest_data_dir
from JloXml import XmlUtils

class CurriculumRecord (BackPackMetadataMixin, ConceptsRecord):
	id_prefix = 'BP-CURR'
	xmlFormat = 'concepts'
	collection = 'curricula_bp'
	xmlTemplate = 'CURRICULUM-Template.xml'
	xmlRecordClass = ConceptsRecord
	
	def makeRelation (self, unit):
		"""
		making relation from chapter to topic/concept
		"""
		num = str(len(self.get_relations()) + 1)
		data = {
			'object' : 'Unit',
			'relationship': 'Requires',
			'objectTitle' : unit.shortTitle,
			'num' : num,
			'id' : unit.getId(),
			'idType' : 'CCS'
		}
		print "Curriculum making a relation with data:%s" % data
		return Relation (data=data)
	
class Curriculum (BackPackModelObject):
	"""

	"""
	xmlRecord_constructor = CurriculumRecord
	
	def __init__(self, name, parent=None):
		"""
		path is a tab-delimited curriculum data file`
		"""
		self.name = name
		BackPackModelObject.__init__ (self, parent)
		
		unitData = UnitData (os.path.join (ingest_data_dir, self.name))
		self.unit = Unit(unitData)
		
		
	def getName (self):
		return self.getRecord().getShortTitle()
		
	def getChildren (self):
		"""
		ASSUMPTION: we only have a single child unit
		"""
		return {self.unit.getId(): self.unit}
		
	def getRecord (self):
		"""
		get template record, and then populate with chapter data
		NOTEs:
			- 'object' is set in template
			- ID has to be set before the record can be written
		"""
		if not self.record:
			rec = BackPackModelObject.getRecord(self)
			

			unitRelation = rec.makeRelation(self.unit)
			rec.addRelation (unitRelation)
					
			self.record = rec
			self.write()
			
		return self.record
		
if __name__ == '__main__':
	"""
	Curriculum data is simply a name (which is shared by Org, Curriculm, and Unit)
	"""
	
	# orgCurrUnit = os.listdir(ingest_data_dir)[0]
	
	orgCurrUnit = 'Engineering Class'

	
	c = Curriculum (orgCurrUnit)
	rec = c.getRecord()
	c.write()
	print rec
		
	

	
	
