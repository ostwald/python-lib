"""
shows a single request as three entries.
it really isn't necessary to show as entries, since we don't want
to change the contents.
"""

import sys

if sys.platform == 'win32':
	sys.path.append ("H:/python-lib")
elif sys.platform == 'linux2':
	sys.path.append ("/home/ostwald/python-lib")
else:
	sys.path.append ("/Users/ostwald/devel/python-lib")

from Tkinter import *
from Request import Request, log_entry
from gui import Quitter

request = Request (log_entry)
print request.get_field("id")

fields = 'id', 'prior status', 'current status'

class R_Entry (Entry):
	def __init__ (self, parent, field, **kw):
		Entry.__init__ (self, parent, kw)
		self.field = field

	def get (self):
		return "%s: %s" % (self.field, Entry.get(self))

def fetch (entries):
	for entry in entries:
		print 'Input => "%s"' % entry.get()			# get text

def fillHeader (row, fields):
	for field in fields:
		lab = Label(row, width=25, text=field)		# add label, entry
		row.pack (side=TOP, fill=X)
		lab.pack(side=LEFT, expand=NO, fill=X)

def fillRow (row, fields):
	entries = []
	for field in fields:
		ent = R_Entry(row, field, width=25)
		ent.insert (0, request.get_field (field))
		row.pack(side=TOP, fill=X)					# pack row on top
		ent.pack(side=LEFT, expand=NO, fill=X)	# grow horizontal
		entries.append(ent)
	return entries

if __name__ == '__main__':
	root = Tk()
	fillHeader (Frame (root), fields)

	row = Frame (root)
 	ents = fillRow(row, fields)
 	root.bind('<Return>', (lambda event, e=ents: fetch(e)))	  
 	Button(root, text='Fetch',
 				 command=(lambda e=ents: fetch(e))).pack(side=LEFT)
	Quitter(root).pack(side=RIGHT)
	root.mainloop()
