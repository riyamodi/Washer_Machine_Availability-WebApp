from twilio.rest import TwilioRestClient
import model
from datetime import datetime, timedelta
import time
from sqlalchemy import type_coerce

def text():
	#Account Sid and Auth Token
	account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	#add auth_token back in
	auth_token = "c19556f5039fefb828e2688e1cee25ef"
	client = TwilioRestClient(account_sid, auth_token)

	while True:
		
		#start_time = model.session.query((type_coerce(model.Load.start_time, DateTime).filter_by(machine_id=3)))
		load = model.session.query(model.Load).filter_by(machine_id=3).one()
		print "got start_time as: ", load.start_time
		print "start time type: ", type(load.start_time)

		current_time = datetime.today()
		print "current time is: ", current_time
		print "current time type is: ", type(current_time)
		
		if datetime.now() > timedelta(seconds=30) + load.start_time:
			message = client.sms.messages.create(body="Laundry will be done in 30 seconds", to="+15107898157", from_="+15104021338")
			print "MESSAGE: ", message.sid
			break

		time.sleep(3)

if __name__ == "__main__":
	text()