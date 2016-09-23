import sys

path = "elementOrders.txt"
# path = "badOrders.txt"
orders = []
for line in open(path).read().splitlines():
	orders.append (line.split(','))

print "%d orders read" % len(orders)

def getUniversalOrder ():
	uni = []
	for order in orders:
		for i, tag in enumerate(order):
			if not tag in uni:
				if i > 0:
					insertPt = uni.index(order[i-1]) + 1
				else:
					insertPt = 0
				uni.insert (insertPt, tag)
		## print uni

	return uni


def compareOrders (i1, i2):
	o1 = orders[i1]
	o2 = orders[i2]
	index = -1
	for i, item in enumerate (o1):
		if item in o2:
			n = o2.index(item)
			if n < index:
				print "%d %s" % (i1, o1)
				print "%d %s" % (i2, o2)
				msg = "'%s' in order %d comes out of order in comparison with order %d" % (item, i2, i1)
				raise Exception, msg
			index = n
	return 1

def compareWith (i):
	# print "\ncompare with %d" % i
	for n in range (len (orders)):
		if n != i:
			try:
				compareOrders (i, n)
			except:
				reason = sys.exc_info()[1]
				# print "%d - NOPE" % n
				print "Mismatch between %d and %d: %s\n\n" % (i, n, reason)

def compareAll ():
	for i in range (len (orders)):
		compareWith (i)

def printUniOrder ():
	uni = getUniversalOrder()
	print "Universal Order"
	for u in uni:
		print "\t", u

	print ','.join(uni)

def showSelected ():
	selected = [10, 11, 34, 49]
	for s in selected:
		print "%d %s" % (s, orders[s])
	
if __name__ == "__main__":
	print '\n'.join(orders[-1])
