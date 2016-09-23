
test_collections = ['tos', 'testosm']

collection_params = {
	'instname' : {
		'vocabUrl' : 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/instName.xsd',
		'typeName' : 'instNameType',
		'vocab_field' : [
				'/key//record/contributors/person/affiliation/instName',
				'/key//record/contributors/organization/affiliation/instName'
			]
	},
	
	'eventname' : {
		'vocabUrl' : 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/eventName.xsd',
		'typeName' : 'eventNameType',
		'vocab_field' : '/key//record/general/eventName'
		},
		
	'fundingentity' : {
		'vocabUrl' : 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/fundingEntity.xsd',
		'typeName' : 'fundingEntityType',
		'vocab_field' : '/key//record/classify/fundingEntity'
		},		
		
	'pubname' : [
		{
			'vocabUrl' : 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/pubName.xsd',
			'typeName' : 'pubNameType',
			'vocab_field' : '/key//record/general/pubName'
		},
		{
			'vocabUrl' : 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/NCARbookPubName.xsd',
			'typeName' : 'NCARbookType',
			'vocab_field' : '/key//record/general/pubName'
		}
	]
}
