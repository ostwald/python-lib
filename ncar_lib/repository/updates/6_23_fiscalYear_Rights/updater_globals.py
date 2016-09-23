"""
Global stuff for update
"""

host_configs = {
	# host_name : { prop : name}
	'acorn' : {
		'records_cache' : '/home/ostwald/Documents/NCAR Library/fiscalYear-update-6-24/try2-6-25/records/osm',
		'searchBaseUrl' : "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1",
		'putBaseUrl' : 'http://nldr.library.ucar.edu/schemedit/services/dcsws1-0'
		},
		
	'taos' : {
		'records_cache' : '/Users/ostwald/devel/python-lib/ncar_lib/repository/updates/6_23_fiscalYear_Rights/records/osm',
		'searchBaseUrl' : "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1",
		'putBaseUrl' : 'http://nldr.library.ucar.edu/schemedit/services/dcsws1-0'
		}
	}

archive_collections = [
	'gate',
	'jkuettner',
	'mesalab',
	'nhre',
	'natlballoonfac',
	'unav',
	'vinlally',
	'wwashington',
	'infooffice'
]

oral_history_collections = [
	'ams',
	'ucarncaroralhist'
]

archival_collections = oral_history_collections + archive_collections
