import os, sys
from SpreadSheetReader import NSESDataSet

dataDir = "/home/ostwald/Documents/Syracuse/SAT-analysis/data"

txtDir = os.path.join (dataDir, "txtFiles")
massDir = os.path.join (dataDir, "MAdone_txt")

def NSESDataSetCaller (path):
#    suggestionSetDir = "/home/ostwald/Documents/Syracuse/SAT-eval/data/suggestionSets"
    
    r = NSESDataSet (path)
    r.report()

def NSESDataSets (dir):
    for filename in os.listdir (dir):
        path = os.path.join (dir, filename)
        NSESDataSetCaller (path)


#  append "_done" to the filename root for all files in directory
def renameMAdoneFiles ():

    for filename in os.listdir (massDir):
        root, ext = os.path.splitext (filename)
        src = os.path.join (massDir, filename)
        dstname = root + "_done" + ext
        print "%s -> %s" % (filename, dstname)
        os.rename (src, os.path.join (massDir, dstname))

def singleNSESDataSet ():
    dir = massDir
    filename = "Applied_5-8_S101EF6F_done.txt"
    NSESDataSetCaller (os.path.join (massDir, filename))

def allNSESDataSets ():
    dir = massDir
    NSESDataSets (dir)


if __name__ == "__main__":

    allNSESDataSets()
