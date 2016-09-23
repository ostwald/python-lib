import time, demjson, urllib
import threading
from service_tester import getSurveyDataTest, addRowTester
# baseUrl = 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/instName.xsd'

def threadTarget ():
	getSurveyDataTest()
	addRowTester()

threads = []
for i in range(5):
	t = threading.Thread(target=threadTarget)
	threads.append(t)
	t.start()
	

