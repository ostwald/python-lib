"""
fscmp tester
"""
import os, sys, re
from fscmp import fileCmp, JloFile, WorkingFile, WorkingDirectory

baseDir = '/Users/ostwald/fooberry'
workDir = os.path.join (baseDir, 'working')
refDir = os.path.join (baseDir, 'reference')

def fileCmpTester ():

	filename = 'hello.text'
	
	workingFile = WorkingFile (os.path.join (workDir, filename))
	refFile = JloFile (os.path.join (refDir, filename))
	verbose = True
	
	print fileCmp(workingFile, refFile, verbose)

def workingDirTester ():
	cmp = WorkingDirectory (workDir, refDir)
	cmp.select(['new','missing'])
	print cmp
	
if __name__ == '__main__':
	workingDirTester()
