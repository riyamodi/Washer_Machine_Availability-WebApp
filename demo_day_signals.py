import model
import app
from datetime import datetime, timedelta

def signal(l_id):

	l = model.Load()

	l.machine_id = l_id

	machine = model.session.query(model.Machine).filter_by(id=l.machine_id).one()
	app.add_to_database(l)

	l.machine.in_use = "shaking"
	app.add_to_database(machine)

	l.start_time = datetime.today() + timedelta(weeks=20)
	l.end_time = l.start_time + timedelta(weeks=52)
	app.add_to_database(l)

	print "committed everything--check database"
	
