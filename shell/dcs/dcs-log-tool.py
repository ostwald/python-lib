#!/usr/bin/env python
import sys
import os
import string

tomcatpath = "/dpc/services/dcs/dcs.dlese.org/tomcat"

if not os.path.exists(tomcatpath):
	print "tomcat path does not exist at ", tomcatpath
	sys.exit()

for filename in os.listdir (tomcatpath):
	print filename
