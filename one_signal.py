import model
# import send_text
import urllib
import time
from datetime import datetime, timedelta


def signal():

	vibration = "shaking"
	m_id = 2

	send_url(vibration,m_id)

	#commented out to test texting.py
	#send_text.pre_text(m_id)

	#time.sleep(30)
	time.sleep(30)
	
	#i don't even need this do i
	vibration = "still"

	#i don't even need this do i, i think i do
	#so the page shows that a machine is no longer in use
	send_url(vibration,m_id)

	#commented out to test texting.py
	# send_text.done_text(m_id)

def send_url(vibration, m_id):
	
	urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration, m_id))
	print "ping machine %d as %s" % (m_id,vibration)


# if __name__ == "__main__":
# 	signal()
	
