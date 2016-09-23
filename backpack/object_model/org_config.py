"""
OrgConfig
"""
import os, sys
import bp_share


from backpack.orgConfigRecord import OrgConfigRecord, CurriculumElement, UnitElement, ChapterElement
from curriculum import Curriculum
from backpack.object_model import *
from backpack.data_model import utils, UnitData
from backpack.data_model.backpack_config_data import courses_config
from JloXml import XmlUtils
from backpack.data_model.utils import ingest_data_dir

class OrgConfigMetadataRecord (BackPackMetadataMixin, OrgConfigRecord):
	id_prefix = 'ORG-CONFIG'
	xmlFormat = 'ccs_org_config'
	collection = 'org_config'
	xmlTemplate = 'ORG-CONFIG-Template.xml'
	xmlRecordClass = OrgConfigRecord
	
	def makeCurriculumElement (self, curriculum):
		"""
		  <curricularSelections>
			<curriculum recordId="BP-CURR-000-000-000-001" name="June Session - Anaheim, CA">
			  <unit recordId="BP-UNIT-000-000-000-001" name="Analysis &amp; Testing 2.6.0 Part II">
				<chapter recordId="BP-CHAPTER-000-000-000-002" name="Physics 2.6.0 Part 1"/>
			  </unit>
			  <unit recordId="BP-UNIT-000-000-000-002" name="Pathways &amp; Aerospace Rocketry">
				<chapter recordId="BP-CHAPTER-000-000-000-001" name="Aerodynamic Engineering 2.5.1"/>
			  </unit>
			</curriculum>
		"""
		curriculumElement = CurriculumElement(curriculum.getId(), curriculum.getName())
		for unit in curriculum.getChildren().values():
			unitElement = UnitElement (unit.getId(), unit.name)
			curriculumElement.addChild (unitElement)
			
			for chapter in unit.getChildren().values():
				chapterElement = ChapterElement(chapter.getId(), chapter.shortTitle)
				unitElement.addChild (chapterElement)
				
		return curriculumElement
			
class OrgConfig (BackPackModelObject):
	"""

	"""
	xmlRecord_constructor = OrgConfigMetadataRecord
	
	def __init__(self, name, parent=None):
		"""
		path is a tab-delimited curriculum data file`
		"""
		
		self.name = name
		config_data = courses_config[self.name]
		
		self.orgEntity = config_data['orgEntity']
		self.orgKey = config_data['orgKey']
		
		TopicRecord.dowrites = 1
		ChapterRecord.dowrites = 1
		
		BackPackModelObject.__init__ (self, parent)
			
		# curriculum children are Unit instances
		self.curriculum = Curriculum (self.name)
		
	def getChildren (self):
		"""
		ASSUMPTION: we only have a single child curriculum
		"""
		return {self.curriculum.getId(): self.curriculum}
		
	def getRecord (self):
		"""
		get template record, and then populate with chapter data
		NOTEs:
			- 'object' is set in template
			- ID has to be set before the record can be written
		"""
		if not self.record:
			rec = BackPackModelObject.getRecord(self)
			
			rec.setTitle (self.name)
			rec.setOrgEntity (self.orgEntity, self.orgKey)
			
			curriculumEl = rec.makeCurriculumElement(self.curriculum)
			rec.addCurriculumElement (curriculumEl)
					
			self.record = rec
			self.write()
			
		return self.record
		
def singleOrg (orgCurrUnit):
	# orgCurrUnit = os.path.join (ingest_data_dir, name)

	org = OrgConfig (orgCurrUnit)
	rec = org.getRecord()
	org.write()
	print rec
		
if __name__ == '__main__':
	"""
	Each Unit (corresponding to the directories in "ingest_data_dir") are represented
	by a single OrgConfig and a single Cirriculum (in addition to a Unit record)
	"""
	if 0:
		name = 'Engineering Class'
		singleOrg (name)
		
	else:
		
		for orgCurrUnit in os.listdir (ingest_data_dir):
		
			org = OrgConfig (orgCurrUnit)
			rec = org.getRecord()
			org.write()
			print rec
		
	

	
	
