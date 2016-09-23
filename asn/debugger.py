
import os, sys
from Localizer import LOCALIZED, ORIGINAL, getPath
from AsnRecord import AsnRecord, makeFullId
from AsnStandard import AsnStandard
from StdDocument import StdDocument
from util import *

filename = "1995-Colorado-Science.xml"
path = getPath (LOCALIZED, "science", filename)

asn = StdDocument (path)

std = asn[makeFullId("S100C617")]

print std.toString()

for key in asn.keys():
	#print key
	pass



