"""
GOAL: 
	- given a upid and date, return affiliation info
	
other goals: 
	- do all PEIDs have upid? - yes (all but those purged)

iVantage spreadsheet has data in the following form

Name				PEID	Location Start Date		Location End Date	Entity	Lab		Org Unit	DivProg		Div Code	
Abato, Christine M	10005	1/5/87					8/25/89				NCAR	ESSL	HAO			E03			12	

Each record describes are position. 

People are identified by PEID, which are in the peopleDB but not accessible via websearch.
- this mapping IS available in myPhpAdmin and has been exported to "internal_person.txt" which
- how bout service?

How about:
	filename = upid
	contents = history (all records for that upid)
	
xml

<positionHistory>
	<person upid="xxx" peid="xxx">
		<position 
			start="xxx" 
			end="xxx">
			entity=""
			lab=""
			org =""
			divProg =""
			divCode ="" />
	</person>
	...
<positionHistory>
	
"""
from JloXml import XmlRecord, XmlUtils
from joined_data import JoinedData

class PositionHistoryRecord (XmlRecord):
	"""
	reads an tab-delimited File and writes an XML File (see positionHistory above
	"""
	def __init__ (self):
		XmlRecord.__init__ (self, xml="<positionHistory/>")
		self.data = JoinedData()
		for upid in self.data.keys():
			
			# print upid
			personEl = XmlUtils.addElement (self.dom, self.doc, 'person')
			personEl.setAttribute ('upid', str(upid))
			
			for i,ivRec in enumerate(self.data[upid]):
				if i == 0:
					personEl.setAttribute ('peid', str(ivRec.peid))
				posEl = XmlUtils.addElement (self.dom, personEl, 'position')
				for attr in ['start', 'end', 'entity', 'lab', 'org', 'divProg', 'divCode']:
					posEl.setAttribute (attr, str(getattr (ivRec, attr)))

if __name__ == '__main__':
	rec = PositionHistoryRecord()
	rec.write ("POS_HISTORY.xml", pretty=True)
	
