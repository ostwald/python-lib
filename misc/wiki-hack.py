#!/usr/bin/python
#
# Reads from standard input, dumps it onto a Confluence page
# You'll need to modify the URL/username/password/spacekey/page title
# below, because I'm too lazy to bother with argv.
import sys
from xmlrpclib import Server

server = "https://wiki.ucar.edu"
username = "ostwald"
password = ")matic~"
spacekey = "~ostwald"
pagetitle = "my test"

def writeToPage ():
	# Read the text of the page from standard input


##	content = sys.stdin.read()
##  s = Server("http://confluence.example.com/rpc/xmlrpc")
## 	token = s.confluence1.login("username", "password")
## 	page = s.confluence1.getPage(token, "SPACEKEY", "Page Title")

	content = "hello world!"
	s = Server(server + "/rpc/xmlrpc")
	token = s.confluence1.login(username, password)
	page = s.confluence1.getPage(token, spacekey, pagetitle)
	page["content"] = content
	s.confluence1.storePage(token, page)


def createPage ():
	newpage = {"title":"New Page","content":"new content","space":"spaceKey"}
	newpage = s.confluence1.storePage(token, mypage);

writeToPage()
