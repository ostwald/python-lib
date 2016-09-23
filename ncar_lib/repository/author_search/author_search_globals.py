CERTAIN_CONFIDENCE = 5
HIGH_CONFIDENCE = 3
LOW_CONFIDENCE = 1
NO_CONFIDENCE = -1


strength_of_matches = {
	CERTAIN_CONFIDENCE : 'certain',
	HIGH_CONFIDENCE : 'strong',
	LOW_CONFIDENCE : 'weak',
	NO_CONFIDENCE : 'none',
}

from author import Author
default_baseUrl = 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1'

# -------------- testing data -------------------
# par authors
Phil_Judge = Author ('Judge', 'Phil')
Jenny_Sun = Author ('Sun', 'Jielun', upid='4458')
Keith_MacGregor = Author ('MacGregor', 'Keith')

# TESTER = Author ('Strong', 'Mike')
TESTER = Author ('Gille', 'John')
# TESTER = Author ('Gille', 'John', 'C', '13422')
