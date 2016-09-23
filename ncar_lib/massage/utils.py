import os
from ncar_lib.lib import globals

def rec_cmp (rec1, rec2):
	return cmp (rec1.doc.toxml(), rec2.doc.toxml())
	
def validateField (field, field_list=globals.library_dc_fields):
	if not field in field_list:
		msg = "bogus field: '%s'" % field
		raise Exception, msg
	
def lib_webcat_diff (lib_dc, webcat):

	if not lib_dc.getId() == webcat.getId():
		raise Exception, "Mismatching IDS!"
	
	skip_fields = ["dateOfOriginal", 
				   "date",
				   "accessLevel", 
				   "url", 
				   "title", 
				   "fullTitle", 
				   "description", 
				   "fullDescription"]
	
	print "\n---------------------------------"
	print lib_dc.getId()
	for web_field in globals.webcat_fields:
		if web_field in skip_fields: continue
		webcat_vals = webcat.getFieldValues (web_field)
		webcat_vals.sort()
		
		if not globals.field_mapping.has_key (web_field): continue
		
		dc_field = globals.field_mapping [web_field]
		dc_vals = lib_dc.getFieldValues (dc_field)
		dc_vals.sort()
		
		if webcat_vals != dc_vals:
			print ""
			print "\t %s (webcat) %s" % ( web_field, webcat_vals)
			print "\t %s (lib_dc) %s" % ( dc_field, dc_vals	)
			
def webcat_diff (rec1, rec2, rec1name="rec1", rec2name="rec2", field_list=globals.webcat_fields):
	rec_diff (rec1, rec2, rec1name, rec2name, field_list)
		
def library_dc_diff (rec1, rec2, rec1name="rec1", rec2name="rec2", field_list=globals.library_dc_fields):
	rec_diff (rec1, rec2, rec1name, rec2name, field_list)
	
def rec_diff (rec1, rec2, rec1name, rec2name, field_list):
	
	if not rec1.getId() == rec2.getId():
		raise Exception, "Mismatching IDS!"
		

	indent = "  "
	diffFields = []
	for field in field_list:
		rec1_vals = rec1.getFieldValues (field)
		rec2_vals = rec2.getFieldValues (field)
		
		rec1_vals.sort()
		rec2_vals.sort()

		if rec1_vals != rec2_vals:
			diffFields.append (DiffField (field, rec1_vals, rec2_vals, rec1name, rec2name))
			
	if diffFields:
		print "\n-------------------------"
		print rec1.getId()
		for diff in diffFields:
			diff.report()
				
def conversion_diff (rp, rec2):
	"""
	report only records where either:
		there are more values in rec1 than rec2
		OR
		there values in rec1 that are NOT also in rec2
	rec1
	"""
	rec1name = "current"
	rec2name = "converted"
	
	field_list = globals.library_dc_fields
	rec1 = rp.lib_dc_rec
	if not rec1.getId() == rec2.getId():
		raise Exception, "Mismatching IDS!"
		
	diffFields = []
	for field in field_list:
		rec1_vals = rec1.getFieldValues (field)
		rec2_vals = rec2.getFieldValues (field)
		
		rec1_vals.sort()
		rec2_vals.sort()
		
		if len(rec1_vals) > len(rec2_vals):
			diffFields.append (DiffField (field, rec1_vals, rec2_vals, rec1name, rec2name))
			continue
			
		for val in rec1_vals:
			if not val in rec2_vals:
				diffFields.append (DiffField (field, rec1_vals, rec2_vals, rec1name, rec2name))
			exit
	if diffFields:
		print "\n-------------------------"
		print "%s (%s)" % (rec1.getId(), rp.accessionNum)
		for diff in diffFields:
			diff.report()
				
class DiffField:
	indent = "  "
	
	def __init__ (self, field, rec1_vals, rec2_vals, rec1name="rec1", rec2name="rec2"):
		self.field = field
		self.rec1_vals = rec1_vals
		self.rec2_vals = rec2_vals
		self.rec1name = rec1name
		self.rec2name = rec2name
		
	def report (self):
		print "\n%s" % self.field
		# print "\t%s: %s" % (rec1name, rec1_vals)
		# print "\t%s: %s" % (rec2name, rec2_vals)
		print "%s%s" % (self.indent, self.rec1name) 
		for val in self.rec1_vals:
			print "\t'%s'" % val
		print "%s%s" % (self.indent, self.rec2name) 
		for val in self.rec2_vals:
			print "\t'%s'" % val
