import re

namePat = re.compile('([\w^,]+), ([\w]+)')

# foo = 'Igarashi, T, Nakamura, K, Shimoda, H, Tanaka, T, Burrows, JP, Nakajima, T, Talagrand, O'
foo = 'Alexandrov, VN, VanAlbada, GD, Sloot, PMA, Dongarra, J'

def simpleMatch (s):
	m =  namePat.match (s)
	if m:
		print "lastname: %s,  initial: %s" % (m.group(1), m.group(2))
	else:
		print "NO match"

def parse (s):
	print "parsing: %s" % s
	names = []
	i = 0
	buff = s
	cnt = 0
	while 1:
		# print "\n%s" % buff
		m = namePat.search (buff)
		if not m:
			break
		buff = buff[m.end():].strip()

		lastname = m.group(1)
		initials = m.group(2)

		print "lastname: %s,  initial: %s" % (lastname, initials)

		

		if len(initials) == 2:
			initials = "%s.%s." % (initials[0], initials[1])
	   	if len(initials) == 1:
			initials = "%s." % initials[0]
		name = '%s%s' % (initials,lastname)
		print "--> %s" % name
		names.append (name)
	return ', '.join (names)


if __name__ == '__main__':
	names = parse (foo)
	print "\n%s" % names
