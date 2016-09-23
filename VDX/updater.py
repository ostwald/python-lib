import os, sys

import collections

print (dir (collections))

import collections

def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

default = {'x':5, 'line':{'weight':'2', 'color':'blue'}}

args = {'x':2, 'y':3, 'line':{'weight':1}}

opts = default.copy()

opts = update(opts,args)

print opts
