
import random
import urllib
import time
import model

def sensor():

	vibration = "still"

	while True:
		
		id = random.randint(6,52)
		
		if vibration == "shaking":
			vibration = "still"
		else:
			vibration = "shaking"
		urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration,id))
		print "ping machine %d as %s" %(id,vibration)
		time.sleep(10)


if __name__ == "__main__":
	sensor()
	