import model
import urllib
import time
from datetime import datetime, timedelta



def signal():

	# if vibration == "shaking":
	# 	vibration = "still"
	# else:
	# 	vibration = "shaking"

	vibration = "shaking"

	urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=3" % vibration)
	print "ping machine 3 as %s" % vibration

	time.sleep(45)

	# if vibration == "shaking":
	# 	vibration = "still"
	# else:
	# 	vibration = "shaking"

	# urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=3" % vibration)
	# print "ping machine 3 as %s" % vibration

if __name__ == "__main__":
	signal()
	
