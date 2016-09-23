from misc.titlecase import titlecase

def getWOSValues ():
	"""
	read WOS values from a file (normalizing on the way)
	"""
	path = '../uniqueWOSvalues_pubname.txt'
	s = open(path).read()
	raw = s.split('\n')
	values = []
	for v in raw:
		if not v.strip(): continue
		values.append(normalizeItem (v));
	return values
		

def normalizeItem (item):
	s = titlecase (item.lower())
	# s = s.replace ("&", "&amp;")
	return s.strip()
	
def normalizeList (l):
	return map (lambda x: normalizeItem(x), l)
	
def diffLists (list_1, list_2):
	"""
	what items are present in list_1 but not in list_2)
	"""
	ret = []
	# print "ret has %d items" % len (ret)
	list_2_lower = listToLower (list_2)
	for item in list_1:
		if not item.lower() in list_2_lower:
			ret.append(item)
			# print 'non-dup: %s' % item
	ret.sort(lambda a,b: cmp (a.lower(), b.lower()))
	return ret
	
def mergeLists (base, tomerge):
	"""
	add those items in tomerge that aren't present in base
	sort by lower case
	"""
	# intitialze ret by copying base
	ret = []
	map (lambda x: ret.append(x), base)
	
	# print "ret has %d items" % len (ret)
	baseLower = listToLower (ret)
	for item in tomerge:
		if not item.lower() in baseLower:
			ret.append(item)
			# print 'non-dup: %s' % item
	ret.sort(pubNameCmp)
	return ret
	
def listToLower (l):
	return map (lambda x: x.lower(), l)
	
def pubNameCmp (a, b):
	return cmp (a.lower(), b.lower())
	
if __name__ == '__main__':
	list_1 = ['a', 'b', 'c', 'd','D']
	list_2 = ['a', 'e']
	print "merge"
	for item in mergeLists (list_1, list_2):
		print item
		
	print "diff"
	for item in diffLists (list_1, list_2):
		print item
