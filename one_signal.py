import model
import send_text
import urllib
import time
from datetime import datetime, timedelta



def signal():

	vibration = "shaking"
	m_id = 3

	send_url(vibration,m_id)

	# urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration, m_id))
	# print "ping machine %d as %s" % (m_id,vibration)

	send_text.pre_text(m_id)

	time.sleep(30)
	
	vibration = "still"

	send_url(vibration,m_id)

	send_text.done_text(m_id)

	# urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration, m_id))
	# print "ping machine %d as %s" % (m_id,vibration)

	# if machine.type == "Dryer":
	# 	time.sleep(30)
	# 	vibration = "still"
	# 	urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration, m_id))
	# 	print "ping machine %d as %s" % (m_id,vibration)

def send_url(vibration, m_id):
	
	urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration, m_id))
	print "ping machine %d as %s" % (m_id,vibration)



	

	#time.sleep(45)

	# if vibration == "shaking":
	# 	vibration = "still"
	# else:
	# 	vibration = "shaking"

	# urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=3" % vibration)
	# print "ping machine 3 as %s" % vibration

if __name__ == "__main__":
	signal()
	
