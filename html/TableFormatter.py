import sys, os

from HyperText.HTML40 import *

def formattedTable(items, rows, cols):

	html = DIV (id="addresses")
	table = TABLE ()
	html.append(table)
	row = TR()
	cell = TD()
	row.append (cell)
	table.append (row)

	for cnt in range (len (items)):
		print cnt
		# cell.append ( (DIV ("%d - %s" % (cnt, self.data[cnt].asHtml()))))
		cell.append (items[cnt])
		if cnt % rows == rows - 1:
			print "\t adding new cell"
			cell = TD()
			row.append (cell)
		if cnt % (cols * rows) == (cols * rows) - 1:
			print "\t adding new table"
			table = TABLE()
			html.append (table)
			row = TR ()
			cell = TD()
			table.append (row)
			row.append(cell)
	return html
	
def formattedListing(items, cols):
	cols = 2
	table = TABLE ()
	row = TR()
	table.append (row)
	for cnt in range (len (items)):
		row.append ( TD (items[cnt]))
		if cnt % cols == cols - 1:
			row = TR()
			table.append (row)
	return table
