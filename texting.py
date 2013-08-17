import floor_text
import time
import model
from sqlalchemy import desc


#QUESTION: to keep texting.py always running, do I just put the
#code below in one big while loop?

status = "not done"

while (status == "not done"):
	#get request from Database
	#requested_machine = model.session.query(model.Waiting_List).first()
	requested_machine = model.session.query(model.Waiting_List).order_by(desc(model.Waiting_List.id)).first()
	print "requested_machine.id: ", requested_machine.id
	print "requested_machine.machine_type: ", requested_machine.machine_type

	print "calling PRE text"
	response = floor_text.pre_text(requested_machine)

	print "checking first if statement"
	
	if (response[0] == "sent pre_text"):
		print "calling DONE text"
		response2=floor_text.done_text(requested_machine)
		print "sleeping for 30 seconds"
		print "response2[1]: ", response2[1]
		time.sleep(30)
		print "after sleeping, response2[1].in_use: ", response2[1].in_use
		if response2[1].in_use == "still":
			print "WASHER HAS NOT STARTED AGAIN TEXT NEXT PERSON!!!"
			text_body = "was not claimed, it's YOURS"
			floor_text.actual_text(response[1],text_body)
			print "sent wait list text"
		status = "done"
	if (response[0] == "sent done_text"):
		print "should have gotten texts"
		print "the machine that was returned is: ", response[1].id
		print "sleeping for 30 seconds"
		time.sleep(30)
		if response[1].in_use == "still":
			print "WASHER HAS NOT STARTED AGAIN TEXT NEXT PERSON!!!"
			text_body = "was not claimed, it's YOURS"
			floor_text.actual_text(response[1],text_body)
			print "sent wait list text"
		status = "done"
	

