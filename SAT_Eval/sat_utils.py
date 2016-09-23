
from asn import makeFullId, getNumId
import string

nses_std_domains = {
	"Earth and Space Science" : "D",
	"History and Nature of Science" : "G",
	"Life Science" : "C",
	"Physical Science" : "B",
	"Science and Technology" : "E",
	"Science as Inquiry" : "A",
	"Science in Personal and Social Perspectives" : "F",
	}

domain_groups = {
	"Inquiry" : ['A'],
	"Subject" : ['B', 'C', 'D'],
	"Applied" : ['E', 'F', 'G']
	}

domain_groups_keys = ["Inquiry", "Subject", "Applied"]
	
def band_cmp (a, b):
	"""
	comparator for sorting grade ranges
	"""
	if a[0] == "K": x = "0"
	else: x = a[1]
	if b[0] == "K": y = "0"
	else: y = b[0]
	return cmp (x,y)

state_list = ["Colorado", "Massachusetts", "Minnesota", "New York", "Ohio"]
