"""
comparison manager data - some values to insert in the HTML pages
"""

blurbs = {
	'TitlePubNameMap' : 
	"""<div>The groups listed here are determined by applying a same formula to each record in the <i>PUBS NotFY10</i>
	collection to create a key for each record, and then grouping the records having the same key.
	The formula for creating keys is:</div>
	<ol>
		<li>Obtain a <i>titleFragment</i> by omitting the portion of the title after the last colon (if any).</li>
		<li>Cast the titleFragment to lower case and remove all non-alpha characters</li>
		<li>Append the record's <i>pubName</i> to the key</li>
	</ol>
	<div class="directions">Click on the magnifying glass icon to compare the records within a group</div>""",
	
	'TitleGroupingMap' : 
	"""<div>The groups listed here are determined by applying a same formula to the <i>title</i> of 
	each record in the <i>PUBS NotFY10</i>
	collection to create a key for each record, and then grouping the records having the same key.
	The formula for creating keys is:</div>
	<ol>
		<li>Cast the titleFragment to lower case and remove all non-alpha characters</li>
	</ol>
	<div>NOTE: This method groups together records having similar titles, but there may be many false positives,
	since often articles with similar titles are published in different contexts (and therefore have different pubNames).</div>
	<div class="directions">Click on the magnifying glass icon to compare the records within a group</div>""",
	
	'RecordComparison' :
	"""NOTE: this display is static HTML. The actual record in the DCS may have
	changed since the HTML was generated"""
	
}

titles = {
	'TitlePubNameMap' : 'PUBS NOT FY10 - Duplicate Groups based on Title and PubName',
	'TitleGroupingMap' : 'PUBS NOT FY10 - Duplicate Groups based on Similar Titles'
}
	
def getBlurb (key):
	if blurbs.has_key(key):
		return blurbs[key]
		
def getTitle (key):
	if titles.has_key(key):
		return titles[key]
