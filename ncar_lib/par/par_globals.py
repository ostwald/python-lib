from parAuthor import ParAuthor

default_baseUrl = 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1'

# par authors
Phil_Judge = ParAuthor ('Judge', 'Phil')
Jenny_Sun = ParAuthor ('Sun', 'Jielun', upid='4458')
Keith_MacGregor = ParAuthor ('MacGregor', 'Keith')

# TESTER = ParAuthor ('Strong', 'Mike')
TESTER = ParAuthor ('Gille', 'John')
# TESTER = ParAuthor ('Gille', 'John', 'C', '13422')

Authors_to_run = [
#	ParAuthor ('Jensen', 'Jorgen', upid='4110'), 
#	ParAuthor ('Judge', 'Phil', upid='5652'),
#	ParAuthor ('MacGregor', 'Keith', upid='5503'),
	ParAuthor ('Smith', 'Anne', upid='14678'),   # MULTI-MATCH
# 	ParAuthor ('Gille', 'John', upid='13422'),
#	ParAuthor ('Garcia', 'Rolando', upid='13333'),
#	ParAuthor ('Tie', 'X', upid='3279'),
#	ParAuthor ('Bonan', 'Gordan', upid='11852'),
#	ParAuthor ('Meehl', 'Gerald', upid='7229'), # was Jerry
	ParAuthor ('Hurrell', 'Jim', upid='100'),   # MULTI-MATCH
# 	ParAuthor ('Gent', 'Peter', upid='11128'),
# 	ParAuthor ('Moeng', 'Chin-Hoh', upid='7783'),
# 	ParAuthor ('Snyder', 'Chris', upid='9671'),
# 	ParAuthor ('Weisman', 'Morris', upid='3318'),
#	ParAuthor ('Smolarkiewicz', 'Piotr', upid='4291'),
# 	ParAuthor ('Sun', 'Jielun', upid='4458') # was Jenny
]

