from twilio.rest import TwilioRestClient
import model
from datetime import datetime, timedelta
import time
from sqlalchemy import type_coerce

def pre_text(m_id):
	#Account Sid and Auth Token
	account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	#add auth_token back in
	auth_token = " "
	client = TwilioRestClient(account_sid, auth_token)

	while True:
		
		#start_time = model.session.query((type_coerce(model.Load.start_time, DateTime).filter_by(machine_id=3)))
		load = model.session.query(model.Load).filter_by(machine_id=m_id).one()
		print "got start_time as: ", load.start_time

		current_time = datetime.today()
		print "current time is: ", current_time

		machine = model.session.query(model.Machine).filter_by(id=m_id).one()

		if machine.type== "Washer":
			if datetime.now() > timedelta(seconds=30) + load.start_time:
				message = client.sms.messages.create(body="Washer will be available in 30 seconds", to="+15107898157", from_="+15104021338")
				print "MESSAGE: ", message.sid
				break
		if machine.type == "Dryer":
			if datetime.now() > timedelta(seconds=60) + load.start_time:
				message = client.sms.messages.create(body="Dryer will be available in 30 seconds", to="+15107898157", from_="+15104021338")
				print "MESSAGE: ", message.sid
				break

		time.sleep(3)

def done_text(m_id):
	#Account Sid and Auth Token
	account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	#add auth_token back in
	auth_token = " "
	client = TwilioRestClient(account_sid, auth_token)

	machine = model.session.query(model.Machine).filter_by(id=m_id).one()
	
	if machine.type== "Washer":
		message = client.sms.messages.create(body="Washer is available", to="+15107898157", from_="+15104021338")
		print "MESSAGE: ", message.sid

	if machine.type== "Dryer":
		message = client.sms.messages.create(body="Dryer is available", to="+15107898157", from_="+15104021338")
		print "MESSAGE: ", message.sid




if __name__ == "__main__":
	text()