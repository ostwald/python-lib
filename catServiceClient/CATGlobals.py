# baseUrl = "http://cat.nsdl.org:8280/casaa/service.do"

common_params = {
	"endGrade": "12",
	"query": "http://ga.water.usgs.gov/edu/earthrivers.html",
	"topic": "Science",
	"startGrade": "1",
	"maxResults": "10",
	"author": "National Science Education Standards (NSES)"
	}

suggest_standards_params = {
	"method": "suggestStandards",
	}
suggest_standards_params.update (common_params)

more_like_these_params = {
	"method": "moreLikeTheseStandards",
	"suggestedStandards": [
	    "http://purl.org/ASN/resources/S100ABE0",
        "http://purl.org/ASN/resources/S101369E"]
	}
more_like_these_params.update (common_params)

# params to test the pre-k grade level
preKParams = {
	"query": "http://volcano.oregonstate.edu/",
	"startGrade": "-1",
	"endGrade": "-1",
	"maxResults": "10",
	"topic": "Math",
	"author": "Florida"
	}

servers = {
	'cornell' : { 
		'baseUrl' : "http://cat.nsdl.org:8280/casaa/service.do",
		'username': 'test',
		'password': 'p'
	},
	
	'cnlp' : { 
		'baseUrl' : "http://grace.syr.edu:8080/casaa/service.do",
		'username': 'nsdl',
		'password': 'digi!lib'
	}
}
