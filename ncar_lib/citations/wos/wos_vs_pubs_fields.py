
"""

wos2pubs_fields
	KEYS are field names as they appear in the tab-delimited WOS data files.
	MAPPINGS are human-readable labels
		- lower case field mappings are passed straight through without processing
		(these correspond to pubs fields)
		- Capitalized mappings are processed
		
pubs_publication_fields
	taken from pubs schema - not all fields below are useful
	NOTE: I don't think this data structure is used
"""
wos2pubs_fields = {
	'PT' : 'Pub Type',
	'AU' : 'authors',  # 
	'BA' : 'Book Author',
	'ED' : 'editor',
	'TI' : 'Title',
	'SO' : 'pubname',
	'SE' : '',
	'CR' : 'DOI (unknown pubtype)',
#	'PU' : '? Date - Mo.',
#	'PI' : '? Date - Yr.',
#	'PA' : '? Date - Day',
	'SN' : 'ISSN #',
	'BN' : 'ISBN Number',
	'DI' : 'DOI - Journal',
	'PD' : 'Pub-date',
	'PY' : 'Pub-Year',
	'VL' : 'Volume',
	'IS' : 'Issue',
	'PN' : 'Part Name',
	'SU' : 'Supplement ',
	'SI' : 'Special Issue',
	'BP' : 'begin-page',
	'EP' : 'end-page',
	'UT' : 'wos_id'
}

# taken from pubs schema - not all fields below are useful
pubs_publication_fields = {
	'Publication' : [
		'Pub_ID',
		'Title',
		'Year',
		'PubName_ID',
		'Publisher_ID',
		'MeetSponsor',
		'Editor',  # this is a string field, e.g., "T. B. Gatski, C. G. Speziale, and S. Sarkar"
		'Volume',
		'Pages',
		'DOI',
		'URL',
		'PubStatus',
		'StatusDate',   # YYYY-MM - Use to calculate fiscal year for ASR
		'MeetStartDate',
		'MeetEndDate',
		'Class',
		'Type',
		'MeetCity',
		'MeetStateProvName',
		'MeetCountryCode',
		'Timestamp',
		'ModifiedBy',
		'Collaboration',
		'MeetDate'
		],
	'Author' : [  # use "pub_id" to find the authors for a particular publication
		'Pub_ID',
		'LastName',
		'FirstName',
		'MiddleName',
		'AuthorOrder',
		'Person_ID',
		'Timestamp',
		'ModifiedBy',
		],
		
	'Publisher' : [
		'Publisher_ID',
		'Publisher', 
		'Timestamp',
		'ModifiedBy',
		],
		
	'PubName' : [		
		'PubName_ID',
		'PubName',
		'PubAbbrev',
		'Timestamp',
		'ModifiedBy',
		],
		
	'PubSponsor' : [		
		'PubID',
		'PubFundedOrg',
		'ModifiedBy',
		'Timestamp',
	]
}
	

