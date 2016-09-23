"""
TabDelimitedRecord - 

created from
  -- textline a tab-delimited line of text (e.g., from a spreadsheet) that
  provides the DATA 
  -- schema (list of fields)

provides mapping interface to fields
"""

import os
from string import split, join, strip
from UserDict import UserDict
from UserList import UserList
from HyperText.HTML40 import *

class TabDelimitedRecord:
	"""
	A record consisting of a list of data values, and a schema that provides
	field names and accessors to the data
	"""
	def __init__ (self, data, parent):
		"""
		data - a list of values
		parent - an object that has a 'schema' attribute
		"""
		self.data = data
		self.parent = parent
		# self.schema = FieldList (schema)
		# self.setSchema (schema)

	def __getitem__ (self, field):
		"""
		Provides field-based addressing so that values can be obtained by field name.
		Returns the empty string if the field is not found in the schema
		"""
		index = self.parent.schema.getIndex (field)
		# print 'index (%s) : %d' % (field, index)
		if index > -1:
			try:
				## return self.data[index]
				value = self.data[index]
				if len(value) > 1 and \
				   value[0] == value[-1] == "'" or \
				   value[0] == value[-1] == '"':
					value = value[1:-1]
				return value
			except:
				return ""
		else:
			return ""
			
	def __setitem__ (self, field, value):
		"""
		Dict interface for setting field values
		"""
		index = self.parent.schema.getIndex(field)
		while len (self.data) < len (self.parent.schema):
			self.data.append ("")
		try:
			if index > -1 and index < len (self.parent.schema):
				self.data[index] = value
			else:
				msg = "field not found for '%s'" % field
				raise KeyError, msg
		except:
			pass
			
	def hasValue (self, field):
		"""
		returns true if the named field has a non-empty value
		"""
		return self[field].strip() != "" 
			
	def __repr__ (self):
		"""
		Returns a formatted string representation of this entry
		"""
		return self.asTabDelimitedRecord().join (", ")

	# def setSchema (self, schema):
		# self.schema = FieldList(schema)
		
	def asTabDelimitedRecord (self):
		"""
		joins the fields of this record as a list in schema order.
		E.g., used too write the AddressBook to disk
		"""
		fields = [];add=fields.append
		for field in self.parent.schema:
			add (self[field])
		return string.join (fields, '\t')

# class FieldList (UserList):
	# """
	# Represents a Schema as a list of named fields
	# """
	# def __init__ (self, list=[]):
		# UserList.__init__ (self, list)
# 
	# def getIndex (self, field):
		# """
		# returns the index of the named field, or -1 if the field is not contained
		# in the list of fields
		# """
		# if field in self.data:
			# return self.data.index (field)
		# else:
			# return -1
			# 
	# def asTabDelimitedListing (self):
		# return string.join (self.data, '\t')
