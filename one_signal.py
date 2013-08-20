import model
# import send_text
import urllib
import time
from datetime import datetime, timedelta


def signal():

	vibration = "shaking"
	m_id = 2

	send_url(vibration,m_id)

	time.sleep(60)
	
	vibration = "still"

	send_url(vibration,m_id)

def send_url(vibration, m_id):
	
	urllib.urlopen("http://localhost:5000/load_info?vibration=%s&id=%d" % (vibration, m_id))
	print "ping machine %d as %s" % (m_id,vibration)


if __name__ == "__main__":
	signal()
	
