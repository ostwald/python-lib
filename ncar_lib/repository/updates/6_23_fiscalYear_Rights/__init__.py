"""
FiscalYear update - see https://wiki.ucar.edu/x/RLqTB

For the Archives and Oral Histories collections, add N/A to EVERY record to
/record/coverage/fiscalYear

For all other OSM formated collections act only on DONE records and use fiscal.
If no fiscal, then use published first. If no published, use created.

case 1 - archives
  - scope - Archives and Oral Histories collections
  - action - set fiscalYear to N/A for EVERY record
  
case 2 - all other OSM collections

  - scope - done records in all other OSM collections
  - action - use the record's date field (/record/coverage/date) to determine fiscalYear:

    * use fiscal if possible (converting to YYYY if necessary)
    * If no fiscal, then use published first.
    * If no published, use created.
"""
