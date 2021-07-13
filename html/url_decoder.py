"""
print out url's decoded parameters, etc
"""
import query_util

path = '/Users/ostwald/tmp/query_decode_data.txt'

url = open (path, 'r').read().strip()

# print url
qu = query_util.QueryUtil(url)


print '\nPARAMS'
qu.report(qu.params)

# del (qu.params['ky'])

print qu.makeQueryStr(qu.params)

## now this is WOS stuff
# KeyUT=WOS:000xxxxxxx