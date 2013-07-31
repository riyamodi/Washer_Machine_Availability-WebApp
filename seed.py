import model
import csv
import re

def load_machines(session):

	machines_data = open("seed_data/u.machine")
	machine_list = csv.reader(machines_data, delimiter = "|")

	machines = []

	for row in machine_list:
		print row
		m = model.Machine(id=row[0],type=row[1],in_use=row[2],location_id=row[3])
		machines.append(m)

	for m in machines:
		session.add(m)

	session.commit()

def load_locations(session):

	locations_data = open("seed_data/u.location")
	location_list = csv.reader(locations_data, delimiter = "|")
	
	locations = []

	for row in location_list:
		print row
		l = model.Location(id=row[0],school=row[1],dorm=row[2],dorm_address=row[3],floor=row[4])
		locations.append(l)

	for l in locations:
		session.add(l)

	session.commit()

def load_users(session):

	users_data = open("seed_data/u.user2")
	user_list = csv.reader(users_data, delimiter = "|")

	users = []

	for row in user_list:
		cellphone_num = row[4]
		cellphone_num = re.sub("[( ) -]","", cellphone_num)
		u = model.User(id=row[0],location_id=row[1],email=row[2],password=row[3],
						cellphone_num=cellphone_num)
		users.append(u)
		print "list of user info: ", users

	for u in users:
		session.add(u)

	session.commit()

def main(session):
	load_machines(s)
	load_locations(s)
	load_users(s)

if __name__ == "__main__":
	# s=model.connect()
	s=model.session
	main(s)