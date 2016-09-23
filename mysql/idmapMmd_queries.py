import os, sys, string
from IdmapDB import BolideDB, WebTestDB

table = "idmapMmd"
collection = "dwel"

db = WebTestDB()
schema = db.getSchema (table)

# first lets get results for a list of records
# this approach takes same time as getting record for one id
ids = [
	"DWEL-000-000-000-045",
	"DWEL-000-000-000-097",
	"DWEL-000-000-000-149",
	"DWEL-000-000-000-254",
	"DWEL-000-000-000-271",
	"DWEL-000-000-000-273",
	"DWEL-000-000-000-378",
	"DWEL-000-000-000-379",
	"DWEL-000-000-000-380",
	"DWEL-000-000-000-388",
	"DWEL-000-000-000-402",
	"DWEL-000-000-000-444"
	]

def getIdClause ():
	if not ids:
		return ""
	s=[];add=s.append
	for id in ids:
		add ("id='%s'" % id)
	return " or ".join (s)



query = "SELECT *  FROM %s WHERE %s" % (table, getIdClause())

rows = db.doSelect (query)
for record in rows:
	print record[schema.index('id')], len (record[schema.index('primaryContent')])


