"""
This package aims to pull DDS Repository functionality out of the
places where it is implemented in a specific context but is actually
relevant here (a broader context).
- the prime example is ncar_lib.repository. And this is where we'll start
"""

from search import NoMatchingRecordsException, RepositorySearcher
from search_result import StoredContent, SearchResult
