import os, time
import sys

path = "/Volumes/Info_Space/Originals/2002-tmp"

if not os.path.exists(path):
	print path + " does not exist"
	sys.exit();

lastMod = os.path.getmtime (path)
print "lastMod", lastMod
print  time.ctime(lastMod)

year = 2004
month = 4
day = 23
hour = 12
minute = 59
second = 0

tuple = (year, month, day, hour, minute, second, -1, -1, -1)
mytime = time.mktime(tuple)

print "mytime", mytime
print "mydate", time.ctime(mytime)
print int(mytime)

## set the acces and modified time of the file at path
os.utime (path, (mytime, mytime))

