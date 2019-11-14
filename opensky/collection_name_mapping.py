import os, sys, re

path = '/Users/ostwald/Sites/archives/mappings.txt'

lines = open(path, 'r').read().split('\n')

print 'collection_name_mapping= {'
for l in lines:
    splits = l.split('\t')
    if len(splits) < 2:
        continue
    print "\t'%s': '%s'," % (splits[0], splits[-1])
print '}'