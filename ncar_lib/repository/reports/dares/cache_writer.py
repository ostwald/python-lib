import os, sys
from ncar_lib.repository.record_manager import CachingRecordManager, CachedRecordError

import ncar_lib
ncar_lib_dir = os.path.dirname (ncar_lib.__file__)

metadata_cache = os.path.join (ncar_lib_dir, 'repository/reports/dares/records')
searchBaseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
putBaseUrl = "http://nldr.library.ucar.edu/schemedit/services/dcsws1-0"

record_manager = CachingRecordManager(searchBaseUrl=searchBaseUrl, putBaseUrl=putBaseUrl, baseCachePath=metadata_cache)
record_manager.statusNote = "updated dares authors"
record_manager.writeCacheToRemote()
