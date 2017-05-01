__author__ = 'ostwald'

import sys, os, requests

orcid = '0000-0002-2510-1225'
url = 'https://api.orcid.org/v1.2/%s/orcid_profile' % orcid
access_token = 'd466d74a-1a9b-466c-8637-e4866fac6427'

headers = {
	'Authorization' : 'Bearer %s' % access_token,
	'Content-type' : 'application/vdn.orcid+xml'
 }

r = requests.get(url, headers=headers)

print r.text