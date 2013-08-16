import model
# import send_text
import urllib
import time
import app
from datetime import datetime, timedelta


def signal(m_id):

	l = model.Load()

	l.machine_id = m_id

	machine = model.session.query(model.Machine).filter_by(id=l.machine_id).one()
	app.add_to_database(l)

	l.machine.in_use = "shaking"
	app.add_to_database(machine)

	l.start_time = datetime.today()
	l.end_time = l.start_time + timedelta(seconds=20)
	app.add_to_database(l)


# if __name__ == "__main__":
# 	signal()
	
