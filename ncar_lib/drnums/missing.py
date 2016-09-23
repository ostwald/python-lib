"""

reads a data file containing the IDS that are managed in DRMappings, but that
are NOT found in the NLDR. These so-called missing records may have been merged
with other records (e.g., when there are multiple "parts" associated with the
same objects) or moved to a different collection (which changes the metadata
record ID, but does NOT change the asset's name or location

Missing is basically a list of record ids.
"""

import os, sys
from UserList import UserList
from line_data_reader import LineDataReader

default_data = "missing.txt"

class Missing (LineDataReader):
	def __init__ (self, data=default_data):
		LineDataReader.__init__ (self, data)
		self.sort()
			
if __name__ == '__main__':
	m = Missing()
	m.report()
