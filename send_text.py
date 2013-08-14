from twilio.rest import TwilioRestClient
import model
from datetime import datetime, timedelta
import time
from sqlalchemy import type_coerce

def actual_text(machine, text_body):
	
	#Account Sid and Auth Token
	account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	#add auth_token back in
	auth_token = " "
	client = TwilioRestClient(account_sid, auth_token)
	
	message = client.sms.messages.create(body="%s %s" %(machine.type, text_body), to="+15107898157", from_="+15104021338")
	print "MESSAGE: ", message.sid


def pre_text(m_id):
	
	while True:
		
		load = model.session.query(model.Load).filter_by(machine_id=m_id).one()
		print "got start_time as: ", load.start_time

		current_time = datetime.today()
		print "current time is: ", current_time

		machine = model.session.query(model.Machine).filter_by(id=m_id).one()

		text_body = "will be available in 30 seconds"

		if machine.type== "Washer":
			if datetime.now() > timedelta(seconds=30) + load.start_time:
				actual_text(machine, text_body)
				break
			
		if machine.type == "Dryer":
			if datetime.now() > timedelta(seconds=60) + load.start_time:
				actual_text(machine, text_body)
				break

		time.sleep(3)

def done_text(m_id):

	machine = model.session.query(model.Machine).filter_by(id=m_id).one()

	text_body = "is AVAILABLE"

	actual_text(machine, text_body)


if __name__ == "__main__":
	text()