"""
scripts to implement PAR report (see https://wiki.ucar.edu/x/KZlCB)

exposes 
	AuthorReporter, AuthorSearchResult, 
	OsmAuthorReporter, OsmAuthorSearchResult,
	personSchema (fields for MetadataAuthor, which represents a "bestMatch")
"""
from author import Author
from authorSearcher import AuthorSearcher, ReporterMixin
from authorSearchResult import AuthorSearchResult, personSchema
from osmAuthorSearcher import OsmAuthorSearcher, OsmAuthorSearchResult
from author_search_globals import CERTAIN_CONFIDENCE, HIGH_CONFIDENCE, LOW_CONFIDENCE, NO_CONFIDENCE, strength_of_matches
