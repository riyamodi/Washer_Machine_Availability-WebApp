import model
#making a dictionary for the locations

def md():

	dictionary={"school":[], "dorms":[ ]}

	schools = model.session.query(model.Location).group_by(model.Location.school).all()
	print "schools: ",schools
	for s in schools:
		print s.school
		dictionary["school"].append(s.school)
	#now I have d={"school":["Georgetown Univeristy", "Fake School"]}
	#but the names are coming out in unicode

	print "dictionary with schools: ", dictionary

	dorms = model.session.query(model.Location).group_by(model.Location.dorm).all()

	print "dorms list: ", dorms

	otherdictionary={}
	floor_list=[]
	for dorm in dorms:
		floor_list.append(model.session.query(model.Location).filter_by(dorm=dorm.dorm).group_by(model.Location.floor).all())

	print "floor_list: ", floor_list
		#otherdictionary[dorm.dorm]=(model.session.query(model.Location).filter_by(dorm=dorm.dorm).group_by(model.Location.floor).all()).floor
	print "length: ", len(floor_list)

	for floor in floor_list:
		print "floor.floor: ", floor.floor
	# print "otherdictionary: ", otherdictionary

	# dictionary["dorms"].append(otherdictionary)

	# print "dictionary: ", dictionary


