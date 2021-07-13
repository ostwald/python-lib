import datetime

if 1:
    # get two pictures taken at the same time and create a delta
    iphone_ref = datetime.datetime(2020, 10, 2, 10, 43, 50)
    canon_ref = datetime.datetime( 2020, 10, 2, 17, 49, 50)

if 0:
    iphone_ref = datetime.datetime(2020, 10, 2, 10, 10, 50)
    canon_ref = datetime.datetime(2020,  10, 2, 10, 40, 50)

delta = iphone_ref - canon_ref
print 'delta', delta

if 0: # test the delta
    test = canon_ref + delta
    print 'test', test,'should be', iphone_ref

if 1:   # apply delta to a picture to get it's adjusted datetime

    canon_pic =  datetime.datetime(2020, 9, 30, 19, 20, 28)

    print 'canon_pic', canon_pic

    adjusted = canon_pic + delta
    print 'adjusted', adjusted

