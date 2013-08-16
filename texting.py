import floor_text
import time
import model

status = "not done"

while (status == "not done"):
	#get location_id from waiting_list
	loc = model.session.query(model.Waiting_List).first()
	print "loc.id: ", loc.id

	print "calling PRE text"
	#commenting this line of code out because line 17 calls the function
	response = floor_text.pre_text(loc.id)

	print "checking first if statement"
	
	if (response == "sent pre_text"):
		print "calling DONE text"
		floor_text.done_text(loc.id)
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


