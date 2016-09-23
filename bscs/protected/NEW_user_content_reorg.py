"""
another stab - this time using scanner to identify records to update

"""
import os, sys, re
import bscs.protected
from metadata_scanner import UserContentScanner
from UserDict import UserDict

bscs.protected.curriculum_view = 'merge'

if __name__ == '__main__':

    baseDir = bscs.protected.getMergeUserContentRepo()
    scanner = UserContentScanner (baseDir)
    scanner.report()
    scanner.writeProtectedUrls()
    # scanner.reportMetadataInfo()
    # scanner.reportRecordMap()

    recordMap = scanner.getRecordMap()
    print "%d records in recordMap" % len(recordMap.keys())

    recordsToUpdate = scanner.recordsToUpdate
    print "%d records to update" % len(recordsToUpdate.keys())
    recordIds = recordsToUpdate.keys()
    recordIds.sort()
    for recordId in recordIds:
        info = recordsToUpdate[recordId]
        print "-", recordId
        for url in info.protectedUrls:
            print '  -', url
