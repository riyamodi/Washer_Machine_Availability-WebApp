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
	
	if (response == "sent pre_text"):
		print "calling DONE text"
		floor_text.done_text(requested_machine)
		status = "done"
	if (response == "sent done_text"):
		print "should have gotten texts"
		status = "done"


	#i can instead check to see if the waiting list column "status". so i have a 
	#pre-text status column and a done-text status column. after one of them get texted
	#in floor_text.py (before the return) update the database. so if pre-text is sent but
	#done-text is not sent, [then call floor_text.done_text(loc.id) NO] continue while loop
	#if both statuses read "sent" then break
	#is sent  then i stop otherwise i keep running this until they are all true


