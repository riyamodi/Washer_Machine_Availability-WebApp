
import random
import urllib
import time
import model


vibration = "still"

while True:
	
	id = random.randint(1,52)
	
	if vibration == "shaking":
		vibration = "still"
	else:
		vibration = "shaking"
	urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration,id))
	print "ping machine %d as %s" %(id,vibration)
	time.sleep(10)


#need to keep track of start time on the sensor side
