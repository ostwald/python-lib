import os, sys, re
import sqlite3
import globals
from comms_db import CommsDBTable

# path_frag_filter = map (lambda x:x.lower(), globals.SKIP_DIR_NAME_FRAGS + globals.SKIP_DIR_NAMES)
path_frag_filter = globals.SKIP_DIR_NAME_FRAGS + globals.SKIP_DIR_NAMES

sqlite_file = '/Users/ostwald/Documents/Comms/FILTERED.sqlite'
db = CommsDBTable (sqlite_file)

for frag in path_frag_filter:
    recs = db.select ('*', "WHERE path like '%{}%'".format(frag))
    print frag, len(recs)