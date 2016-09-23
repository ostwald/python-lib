"""
This modules supports the finding and processing of duplicate records across the NLDR.

Initially, we worry only about finding records with matching titles. 

- The list of unique titles (and their frequencies) is obtained from the NCS via
"ListTerms" service and stored in file "title-term-count.xml". This file is read
by titleTerms.TermList, which creates a Term instance for each entry.

Because there are many 'similar' titles, we crate a secondary representation,
TermMap, which groups similar titles. Similarity is defined by creating key that
eliminate all non-alpha characters from titles. The TermMap maps from each
unique key to all the records whose titles correspond to that key.
"""
from find_dups import CollectionInfo, RecordInfo
