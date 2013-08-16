from twilio.rest import TwilioRestClient
import model
from datetime import datetime, timedelta
import time
from sqlalchemy import type_coerce

def actual_text(m, text_body):
	
	#Account Sid and Auth Token
	account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	#add auth_token back in
	auth_token = "c19556f5039fefb828e2688e1cee25ef"
	client = TwilioRestClient(account_sid, auth_token)
	
	message = client.sms.messages.create(body="%s %s %s at %s %s" %(m.type, m.id, text_body, m.location.dorm, m.location.floor), to="+15107898157", from_="+15104021338")
	print "MESSAGE: ", message.sid


def pre_text(l_id):

	print "in pre_text"
	
	while True:
		
		#get a list of the machines on the page
		machines = model.session.query(model.Machine).filter_by(location_id=l_id).all()
		print "machines: ", machines

		current_time = datetime.today()
		print "current time is: ", current_time

		#go through each machine from the list of machines in a certain location
		for m in machines:
			print "m.id: ", m.id
			print "m.in_use: ", m.in_use
			if m.in_use == "shaking":
				text_body = "will be available in 30 seconds"
				load = model.session.query(model.Load).filter_by(machine_id=m.id).first()
				if m.type== "Washer":
					if datetime.now() > timedelta(seconds=30) + load.start_time:
						actual_text(m, text_body)
						print "sent pre_text for washer"
						return("sent pre_text")
					
				if m.type == "Dryer":
					if datetime.now() > timedelta(seconds=60) + load.start_time:
						actual_text(m, text_body)
						print "sent pre_text for dryer"
						return("sent pre_text")
			
			if m.in_use == "still":
				text_body = "is AVAILABLE"
				actual_text(m, text_body)
				print "sent done_text"
				return("sent done_text")

		time.sleep(3)

def done_text(l_id):

	print "in done_text"

	while True:
		#get a list of the machines on the page
		machines = model.session.query(model.Machine).filter_by(location_id=l_id).all()
		print "machines: ", machines

		print "current time is: ", datetime.today()

		text_body = "is AVAILABLE"

		#go through each machine from the list of machines in a certain location
		for m in machines:
			print "m.id: ", m.id
			print "m.in_use: ", m.in_use
			if m.in_use == "still":
				load = model.session.query(model.Load).filter_by(machine_id=m.id).first()
				print "done load: ", load
				print "done load.end_time: ", load.end_time
				if m.type== "Washer":
					if datetime.now() > load.end_time:
					#if datetime.now() > timedelta(seconds=60) + m.load.start_time:
						actual_text(m, text_body)
						return
					
				if m.type == "Dryer":
					if datetime.now() > load.end_time:
					#if datetime.now() > timedelta(seconds=90) + m.load.start_time:
						actual_text(m, text_body)
						return

		time.sleep(3)

# if __name__ == "__main__":
# 	text()