# coding=utf-8


import re
from UserDict import UserDict

class CharMap (UserDict):

	charMap = {
		193 : "A",
		212 : "o",
		225 : "a",
		227 : "a",
		228 : "a",
		233 : "e",
		237 : "i",
		241 : "n",
		243 : "o",
		244 : "o",
		246 : "o",
		250 : "u",

	}

	def __init__ (self):
		UserDict.__init__(self, self.charMap)

	def OFF__getitem__(self, key):
		if self.data.has_key (key):
			return self.data[key]
		else:
			print "charMap does not have mapping for '%s' (%d)" % (chr(key), key)
			return "?"
		

def showChars (s):
	for ch in s:
		print "'%s' : %d" % (ch, ord(ch))

charMap = CharMap()

# dome provNames have an english/ascii version in square brackets.
# if we find this, return it as the normalized provName
asciiPat = re.compile (r"\[(.*?)\]")

squareBracketPat = re.compile (r"\[.*?\]")

def normalizeProvItem (provItem):
	"""
	japanese provNames have the correct version in square brackets
	this function will change the provName attribute of the provItem
	if it contains extended characters
	"""
	if provItem.countryCode == 'JP':
		m = asciiPat.search(provItem.provName)
		if m:
			provItem.provName = m.group(1).strip()
			
	else:
		provItem.provName = normalize (provItem.provName)
	return provItem

def normalize (s, preparse=0, verbose=1):

	if 0:
		# we can't depend on the square brackets!
		# it works for some: e.g. 'Tôkyô [Tokyo]'
		# but not for all: e.g., 'Isle of Anglesey [Sir Ynys Môn GB-YNM]'
		m = asciiPat.search(s)
		if m:
			return m.group(1).strip()
			
	if preparse:
		# eliminate square brackets:
		m = squareBracketPat.search(s)
		if m:
			s = s.replace (m.group(), '').strip()
			
	
	msgs = [];add=msgs.append
	out = ""
	for ch in s:
		if ord(ch) > 127:
			try:
				out += charMap[ord(ch)]
			except:
				add ( "charMap does not have a mapping for '%s' (%d)" % (ch, ord(ch)))
				out += '?'
		else:
			out += ch
			
	if verbose:
		if msgs:
			print "\nCan't normalize '%s'" % (s)
			for msg in msgs:
				print " - %s" % msg
			
	return out
			
if __name__ == '__main__':
	charMap = CharMap()
	keys = charMap.keys()
	keys.sort()
	for key in keys:
		print '%d : "%s",' % (key, charMap[key])
