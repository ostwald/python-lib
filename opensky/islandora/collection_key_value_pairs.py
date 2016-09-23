import sys, re, os

def line_filter (line):
	if len(line) == 0:
		return 0
	if line[0] == '#':
		return 0
	if len(line) == 0:
		return 0
	return 1

lines = open ('human-readable.txt', 'r').read().split('\n')

lines = filter (lambda x:line_filter(x), map (lambda x:x.strip(), lines))

vocabs = {}

items = []
key = None
for line in lines:
	# print '-', line
	if line.index ('\t') == -1:
		raise Exception, 'tab not found'
		
	splits = filter (None, map (lambda x:x.strip(), line.split('\t')))
	tag = splits[0]
	val = splits[1]
	
	if tag[0] == '!':
		if key:
			vocabs[key] = items
			items = []
		key = tag
		
	else:
		# print '- "%s": "%s"' % (splits[0], splits[1])
		items.append([tag, val])
		# print '<%s>%s</%s>' % (tag, val, tag)
vocabs[key] = items
		
def cmp_val (i1, i2):
	return cmp(i1[1], i2[1])
		
for key in vocabs.keys():
	print '\n%s' % key
	items = vocabs[key]
	items.sort(cmp_val)
	for item in items:
		print '<%s>%s</%s>' % (item[0], item[1], item[0])
