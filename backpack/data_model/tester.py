import os, sys, codecs, re
import urllib
from JloXml import XmlRecord
import utils

# basedir = 'H:/Documents/NSDL/Backpack/ingest/ingest-data-1'
basedir = '/home/ostwald/Documents/NSDL/Backpack/ingest/ingest-data-1'
if not os.path.exists(basedir):
	raise Exception, 'basedir does not exist at %s' % basedir

print '\nunits'
for filename in os.listdir(basedir):
	print '- ', filename
	
unit = "Pathways & Advance Engineering"
# unit = "foo"
unitdir = os.path.join (basedir, unit)

if not os.path.exists(unitdir):
	raise Exception, 'unitdir does not exist at %s' % unitdir
	
print 'unitdir exists!'
	
chapterdir = os.path.join (unitdir, 'Physics 2.6.0 Part 1_files')
if not os.path.exists(chapterdir):
	raise Exception, 'chapterdir does not exist at %s' % chapterdir	

path = os.path.join (chapterdir, 'sheet001.htm')

path = os.path.join (utils.ingest_data_dir, "Pathways & Advance Engineering/Physics 2.6.0 Part 1_files/sheet003.htm")

# path = urllib.quote(path)
# path = path.replace (' ', '\ ').replace('&', '\&')
# path = '"%s"' % path

if not os.path.exists(path):
	raise Exception, 'absolute path does not exist at %s' % path

s = utils.getHtml(path, linesep='\r')
print s
