import os, string
import utils
from ncar_lib.lib import globals, webcatUtils

def recId (rp):
	print rp.recId

def null (rp):
	pass
	
field_list = [
	'dc:title',
	'library_dc:altTitle',
	'dc:description',
	'library_dc:issue'
]

def accessionNumberMapping (rp):
	url = rp.lib_dc_rec.getUrl()
	if url:
		accessionNum = os.path.basename (url)
		print "%s : %s" % (accessionNum, rp.recId)

def showTitleAndAltTitle (rp):
	rec = rp.lib_dc_rec
	titles = rec.getFieldValues ('dc:title')
	altTitles = rec.getFieldValues ('library_dc:altTitle')
	if titles and altTitles:
		print "\n", rp.recId
		showFieldValues ('dc:title', titles)
		showFieldValues ('library_dc:altTitle', altTitles)
		
		# manuscripts case
		if rp.collection == "manuscripts" and len(titles) == 1 and len(altTitles) == 1:
			title = titles[0]
			alt = altTitles[0]
			if title.startswith (alt[:-1]): # some altTitles end in period, some don't
				print "\t ... SWAP ME"
				
		# monographs case
		if rp.collection == "monographs":
			## is there a title element containing 'ASR'?
			ASRTitle = False
			for title in titles:
				if "ASR" in title:
					ASRTitle = True
					continue
			## is there an altTitle containing 'Annual Scientific Report'?
			ASRAltTitle = False
			pat = 'Annual Scientific Report'
			for altTitle in altTitles:
				if pat in altTitle:
					ASRAltTitle = True
					continue
			if ASRTitle and ASRAltTitle:
				print "\t ... SWAP ME"
	
def titlePeriods (rp):
	periods (rp, "dc:title")
	
def altTitlePeriods (rp):
	periods (rp, "library_dc:altTitle")
				
def periods (rp, field="dc:title"):
	rec = rp.lib_dc_rec
	utils.validateField (field)
	field_vals = rec.getFieldValues (field)
	period_vals = []
	for val in field_vals:
		if val[-1] == '.':
			period_vals.append (val)
	if period_vals:
		print "\n%s (%s)" % (rp.recId, field)
		for val in period_vals:
			print "\t'%s'" % val
	
def urlCompare (rp):
	rec = rp.lib_dc_rec
	ncar = rp.ncar_rec
	
	if 1 or rec.getUrl() != ncar.getUrl():
		print "\n", rp.recId
		print "\tworking: " + rec.getUrl()
		print "\tncar: " + ncar.getUrl()
				
def lingo (rp):
	rec = rp.lib_dc_rec
	lingos = rec.getFieldValues("dc:language")
	if lingos and "en" in lingos:
		print "\n", rp.recId
		for l in lingos:
			print "\t", l
			
def rights (rp):
	rec = rp.lib_dc_rec
	pat = "All uses of library resources, including the digitized"
	vocab = "All uses of library resources, including the digitized "
	vocab = vocab + "collections, should be consistent with U.S. Copyright Law."
	rights = rec.getFieldValues("dc:rights")
	if rights:
		for item in rights:
			if item.lower().startswith(pat.lower()) and \
				item != vocab:
				print "\n", rp.recId
				print "\t", item		
				
def subject (rp):
	rec = rp.lib_dc_rec
	subjects = rec.getFieldValues ('dc:subject')
	badsubjects = []
	for subject in subjects:
		if subject[-1] == '.':
			badsubjects.append (subject)
	if badsubjects:
		print "\n", rp.recId
		for subject in badsubjects:
			print "\t", subject
			
def threeWayMatch (rp):
	if altTitleMatchesDescription (rp, False) and \
	   altTitleMatchesTitle (rp, False) and \
	   descriptionMatchesTitle (rp, False):
	   
	   print "\n", rp.recId
	   rec = rp.lib_dc_rec
	   for field in ['dc:title','library_dc:altTitle','dc:description']:
		   showFieldValues (field, rec.getFieldValues (field))

def fieldsHaveMatchingValues (rp, field1, field2, verbose=True):
	utils.validateField (field1)
	utils.validateField (field2)
	rec = rp.lib_dc_rec
	vals1 = map (string.upper, rec.getFieldValues (field1))
	vals2 = map (string.upper, rec.getFieldValues (field2))
	for val in vals1:
		if val in vals2:
			if verbose:
				print "\n", rp.recId
				showFieldValues (field1, vals1)
				showFieldValues (field2, vals2)
			return 1
	return 0

def altTitleMatchesDescription (rp, verbose=True):
	return fieldsHaveMatchingValues (rp, 'library_dc:altTitle', 'dc:description', verbose)
	
def altTitleMatchesTitle (rp, verbose=True):
	return fieldsHaveMatchingValues (rp, 'library_dc:altTitle', 'dc:title', verbose)
	
def descriptionMatchesTitle (rp, verbose=True):
	return fieldsHaveMatchingValues (rp, 'dc:description', 'dc:title', verbose)

def diff (rp):
	utils.library_dc_diff (rp.lib_dc_rec, rp.ncar_rec, "working", "ncar", field_list)

def showFieldValues (field, values):
	indent = "  "
	if not values:
		print "%s%s: None" % (indent, field)
	elif len (values) == 1:
		print "%s%s: '%s'" % (indent, field, values[0])
	else:
		print "%s%s" % (indent, field)
		for val in values:
			print "\t", val
		
def multiFields (rp):
	rec = rp.lib_dc_rec
	
	multis = {}
	for field in field_list:
		utils.validateField (field)
		vals = rec.getFieldValues (field)
		if len(vals) > 1:
			multis[field] = vals
	if multis:
		print "\n", rp.recId
		for field in multis.keys():
			showFieldValues (field, multis[field])
	
def showTitleStuff (rp):
	print "\n%s" % rp.recId
	rec = rp.lib_dc_rec
	for field in field_list:
		utils.validateField (field)
		showFieldValues (field, rec.getFieldValues (field))

def showVocabs (rp):
	print "\n%s" % rp.recId
	rec = rp.lib_dc_rec
	field_list = ["library_dc:instName", 'library_dc:instDivision', 'library_dc:libraryType']
	
	for field in field_list:
		utils.validateField (field)
		showFieldValues (field, rec.getFieldValues (field))
		
def showAltTitle (rp):
	if rp.altTitle:
		print "\n%s\n\taltTitle: %s\n\ttitle: %s\n\tdesc: %s\n\tissue: %s" % \
			(rp.recId, rp.altTitle, rp.title, rp.description, rp.issue)	
	
def showASR (rp):
	if rp.description and "ASR" in rp.description.upper():
		print "\n%s" % rp.recId
		print "\t desc: %s" % rp.description
		print "\t title: %s" % rp.title
		print "\t altTitle: %s" % rp.altTitle
		print "\t issue: %s" % rp.issue
			
def showASRFix (rp):
	if "ASR" in rp.title:
		print "\n%s" % rp.recId
		print "\t desc: %s" % rp.description
		print "\t title: %s" % rp.title
		print "\t altTitle: %s" % rp.altTitle
		print "\t issue: %s" % rp.issue		
		
def showDescription (rp):
	if rp.description:
		print "\n%s\n\tdesc: %s\n\tissue: %s" % (rp.recId, rp.description, rp.issue)
	
def showDescriptionJsp (rp):
	if rp.description and ".jpg" in rp.description.lower():
		print "\n%s\n\tdesc: %s\n\tissue: %s" % (rp.recId, rp.description, rp.issue)
		
def showDescriptionPdf (rp):
	if rp.description and ".pdf" in rp.description.lower():
		print "\n%s\n\tdesc: %s\n\tissue: %s" % (rp.recId, rp.description, rp.issue)

def dupFields (rp):
	rec = rp.lib_dc_rec
	dups = []
	for field in globals.library_dc_fields:
		seen = []
		vals = rec.getFieldValues (field)
		for val in vals:
			if val in seen:
				dups.append (field)
			else:
				seen.append (val)
	if dups:
		print "\n", recId
		for field in dups:
			showFieldValues (field, rec.getFieldValues(field))
	
		
def webcatDates (rp):
	"""
	*dateOfOriginal* and *date* map to *dc:date*
	*dateItemDigitized* maps to *library_dc:date_digitized*
	"""
	webcat = rp.webcat_rec
	do_field = "dateOfOriginal"
	dd_field = "dateItemDigitized"
	d_field = "date"
	do_vals = webcat.getFieldValues (do_field)
	dd_vals = webcat.getFieldValues (dd_field)
	d_vals = webcat.getFieldValues (d_field)
	if do_vals and d_vals or (len (dd_vals) > 1):
		print "\n", rp.recId
		showFieldValues (do_field, do_vals)
		showFieldValues (d_field, d_vals)
		showFieldValues (dd_field, dd_vals)
		
def dates (rp):
	"""
	*dateOfOriginal* and *date* map to *dc:date*
	*dateItemDigitized* maps to *library_dc:date_digitized*
	"""
	rec = rp.lib_dc_rec
	dd_field = "library_dc:date_digitized"
	d_field = "dc:date"
	dd_vals = rec.getFieldValues (dd_field)
	d_vals = rec.getFieldValues (d_field)
	if len (dd_vals) > 0:
		print "\n%s (%s)" % (rp.recId, rp.accessionNum)
		# showFieldValues (d_field, d_vals)
		showFieldValues (dd_field, dd_vals)
