from google import Channel, Notifier, users

# Notifier().send ('jlo', users['jlo'][0])

users = {
	'jlo' : ('jonathan.ostwald@gmail.com','1247065132457'),
	'edtrex' : ('edtrexhub@gmail.com', '1376938899816')
	}

def getChannel_1 (sync=True):
	"""
	'channelID', 'resourceID', 'calendarID', 'messageNum',
	'resourceURI', 'userID', 'ttl'
	"""

	channelNum = 2
	user = 'jlo'
	args = {
		'channelID' : 'channelID-%s-%s' % (channelNum,user),
		'resourceID' : 'channel-%s-1-resourceID' % user,
		'calendarID' : users[user][0],
		'userID' : users[user][1],
		'ttl' : 1
		}
	
	return Channel (args, sync)

def getChannel (user, channelNum, calendarOwner=None, sync=True):
	if calendarOwner is None:
		calendarOwner = user

	args = {
		'channelID' : 'channelID-%s-%s' % (channelNum,user),
		'resourceID' : 'channel-%s-1-resourceID' % user,
		'calendarID' : users[calendarOwner][0],
		'userID' : users[user][1],
		'ttl' : 5
		}
	
	return Channel (args, sync)
	

if __name__ == '__main__':
	doSync = False
	channel1 = getChannel('jlo', 3, sync=doSync)
	channel2 = getChannel('jlo', 4, calendarOwner='edtrex', sync=doSync)
	channel1.send(messageNum=26)
	channel2.send(messageNum=26)
