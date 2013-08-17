from twilio.rest import TwilioRestClient
import model
from datetime import datetime, timedelta
import time
from sqlalchemy import desc

def actual_text(m, text_body):
	
	#Account Sid and Auth Token
	account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	#add auth_token back in
	auth_token = " "
	client = TwilioRestClient(account_sid, auth_token)
	
	message = client.sms.messages.create(body="%s %s %s at %s %s" %(m.type, m.id, text_body, m.location.dorm, m.location.floor), to="+15107898157", from_="+15104021338")
	print "MESSAGE: ", message.sid


def pre_text(requested_machine):

	print "in pre_text"
	
	while True:
		
		#get a list of the machines on the page
		machines = model.session.query(model.Machine).filter_by(location_id=requested_machine.location_id, type=requested_machine.machine_type).all()
		print "machines: ", machines

		current_time = datetime.today()
		print "current time is: ", current_time

		#go through each machine from the list of machines in a certain location
		for m in machines:
			print "m.id: ", m.id
			print "m.in_use: ", m.in_use
			if m.in_use == "shaking":
				text_body = "will be available in 30 seconds"
				load = model.session.query(model.Load).order_by(desc(model.Load.id)).filter(model.Load.machine_id==m.id,model.Load.start_time!=None).first()
				print "load id: ", load.id
				if m.type== "Washer":
					if datetime.now() > timedelta(seconds=30) + load.start_time:
						actual_text(m, text_body)
						print "sent pre_text for washer"
						return("sent pre_text",m)
					
				if m.type == "Dryer":
					if datetime.now() > timedelta(seconds=60) + load.start_time:
						actual_text(m, text_body)
						print "sent pre_text for dryer"
						return("sent pre_text",m)
			
			if m.in_use == "still":
				text_body = "is AVAILABLE"
				actual_text(m, text_body)
				print "sent done_text"
				return("sent done_text", m)
				#return("sent done_text")

			
			model.session.expire(m)


		time.sleep(3)

def done_text(requested_machine):

	print "in done_text"

	while True:
		#get a list of the machines on the page
		machines = model.session.query(model.Machine).filter_by(location_id=requested_machine.location_id, type=requested_machine.machine_type).all()
		#really strange that the below line didn't work....ask why
		#machines = model.session.query(model.Machine).filter_by(location_id=requested_machine.location_id, type=requested_machine.machine_type, in_use="still").all()
		print "machines: ", machines

		print "current time is: ", datetime.today()

		text_body = "is AVAILABLE"

		#go through each machine from the list of machines in a certain location
		for m in machines:
			# print "m.id: ", m.id
			# print "m.in_use: ", m.in_use
			if m.in_use == "still":
			# 	load = model.session.query(model.Load).order_by(desc(model.Load.id)).filter(model.Load.machine_id==m.id, model.Load.start_time!=None).first()
			# 	print "load id: ", load.id
			# 	print "done load.end_time: ", load.end_time
			# 	if datetime.now() > load.end_time:
			# 		actual_text(m, text_body)
			# 		return
				print "m.id: ", m.id
				print "m.in_use: ", m.in_use
				actual_text(m,text_body)
				return("sent done_text", m)

			model.session.expire(m)

		time.sleep(3)

# if __name__ == "__main__":
# 	text()