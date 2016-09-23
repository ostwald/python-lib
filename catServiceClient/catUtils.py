
import re

def stripLearningResourceContent (responseText):
	"""
	remove "LearningResourceContent" from CAT response (the content of the resource)
	Useful because we don't really need to see this and it greatly complicates the response
	"""
	from JloXml.RegExUtils import getTagPattern
	pat = getTagPattern ("LearningResourceContent")
	m = pat.search (responseText)
	if m:
		return responseText.replace (m.group(1), "")
	return responseText
