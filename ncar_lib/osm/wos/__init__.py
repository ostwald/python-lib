"""
Convert WOS tabular data from query results
and convert to osmRecords instances.

Used to support NAR process fall 2011

wos_xls.WosXlsReader - the WOS spreadsheet processor
WosXlsReader extends XlsWorksheet - reads the WOS data spreadsheet that is downloaded from a WOS 
query intended to find all NCAR auths for a given period of time.

Each row of the spreadsheet represents 1 WOS record. The python representation of this row is 
wos_xls.WosXlsRecord. WosXlsRecord takes the row, processes the cell values, and creates an OSM Record. 

- some cells are copied straight to osm without manipulation ('title', 'abstract', 'volume', 'issue')
- the remaining cells are processed in some form before being inserted in the osm record.

SourceXlsReader and SponsorXlsReader are field helpers that do table-lookups on the WOS field value and
replace as necessary from the lookup tables.

The Author class parses the author info from the WOS data and produces the Osm Author Element as XML

"""
# from wos_xls import WosXlsReader
from source_xls import SourceXlsReader
from sponsor_xls import SponsorXlsReader
from wos_author import Author, AuthorParseException
