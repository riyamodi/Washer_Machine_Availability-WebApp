import floor_text
import time
import model

while True:
#get location_id from waiting_list
	loc = model.session.query(model.Waiting_List).first()
	print "loc.id: ", loc.id

	print "calling PRE text"
	floor_text.pre_text(loc.id)

	print "calling DONE text"
	floor_text.done_text(loc.id)

	print "should have gotten texts"


