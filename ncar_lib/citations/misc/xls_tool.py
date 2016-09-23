"""
grab the two top rows of a spreadsheet, where
- row 1 reflects the WOS column headings
- row 2 reflects human-readable label

create python mapping from one to other
"""

import sys, os


wos="PT	AU	BA	ED	TI	SO	SE	CR	PU	PI	PA	SN	BN	DI	PD	PY	VL	IS	PN	SU	SI	BP	EP	UT"
pub="Pub Type	Authors	Book Author	Editor	Title	Journal Title		DOI (unknown pubtype)	? Date - Mo.	? Date - Yr.	? Date - Day	ISSN #	ISBN Number	DOI - Journal	Pub-date	Pub-Year	Volume	Issue	Part Name	Supplement 	Special Issue	begin-page	end-page	WOS ID"

def split_list (l):
	return  l.split('\t')

wos_items = split_list (wos)
print "there are %d wos_items" % len(wos_items)

pub_items = split_list (pub)
print "there are %d pub_items" % len(pub_items)

print "{"
for i, wos in enumerate (wos_items):
	print "\t'%s' : '%s'," % (wos, pub_items[i])
print "}"

