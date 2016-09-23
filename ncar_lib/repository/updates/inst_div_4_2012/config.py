"""
configs
"""
record_manager_config = {

	'local_devel' : {
		'searchBaseUrl' : 'http://localhost:8080/schemedit/services/ddsws1-1',
		'putBaseUrl' : None,
		'data_path' : 'division-name-changes.txt',
		'baseCachePath' : '/Users/ostwald/tmp/updateCache',
	},
	
	'local_update' : {
		'searchBaseUrl' : 'http://localhost:8080/schemedit/services/ddsws1-1',
		'putBaseUrl' : 'http://localhost:8080/schemedit/services/dcsws1-0',
		'baseCachePath' : '/Users/ostwald/tmp/updateCache/osm',
		'indexedSearchBaseUrl' : 'http://localhost:8080/schemedit/services/ddsws1-1',
		'data_path' : 'division-name-changes.txt'
	},
	
	'local_ingest' : {
		'searchBaseUrl' : 'http://localhost:8080/schemedit/services/ddsws1-1',
		'putBaseUrl' : 'http://localhost:8080/schemedit/services/dcsws1-0',
		'baseCachePath' : '/Users/ostwald/tmp/updateCache/osm',
		'data_path' : 'division-name-changes.txt',
		'indexedSearchBaseUrl' : 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1'
	},
	
	'ttambora_devel' : {
		'searchBaseUrl' : 'http://ttambora.ucar.edu:10160/schemedit/services/ddsws1-1',
		'putBaseUrl' : 'http://ttambora.ucar.edu:10160/schemedit/services/dcsws1-0',
		'baseCachePath' : '/Users/ostwald/tmp/updateCache/osm',
		'data_path' : 'division-name-changes.txt',
		'indexedSearchBaseUrl' : 'http://ttambora.ucar.edu:10160/schemedit/services/ddsws1-1'
	},
	
	'tambora_update' : {
		'searchBaseUrl' : 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1',
		'putBaseUrl' : 'http://nldr.library.ucar.edu/schemedit/services/dcsws1-0',
		'baseCachePath' : '/Users/ostwald/tmp/updateCache/osm',
		'data_path' : 'division-name-changes.txt',
		'indexedSearchBaseUrl' : 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1'
	}
	
}
