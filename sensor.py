
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

#how to make this more complicated
#what i want: if a machine is a washer--to send the still message 60 seconds after it's start time
#what i want: if a machine is a dryer--to send the still message 90 seconds after it's start time
