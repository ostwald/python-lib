"""
time utils
"""

import time

def unionDateToStruct (dateStr):
	struct = None
	for format in [ "%Y-%m-%d", "%Y-%m", "%Y" ]:
		try:
			struct = time.strptime (dateStr, format)
			break
		except:
			# print "couldn't parse as ", format
			pass
		
	if not struct:
		raise ValueError, 'could not parse "%s" as a date' % dateStr
				
	# print time.asctime(struct)
	return struct

def unionDateToSecs (dateStr):
	struct = unionDateToStruct(dateStr)
	return int (time.mktime(struct))
