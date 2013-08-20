from math import radians, cos, asin, sqrt, sin
from itertools import imap
import model
import app
import operator


def haversine(lon1, lat1, lon2, lat2):
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	km = 6367 * c
	return km 

# cd() creates a dictionary and saves info to databse
def cd():

	#get all the location ids (that have machines)
	ids = model.session.query(model.Machine.location_id).group_by(model.Machine.location_id).all()
	#convert list of tuples into a list
	list_of_ids = [r for (r,) in ids]
	print "ids: ", list_of_ids
	object_list = []
	#create Location objects for each id
	for i in list_of_ids:
		object_list.append(model.session.query(model.Location).filter_by(id=i).one())
	print "object_list: ", object_list
	print "length of object_list: ", len(object_list)
	d={}
	#iterate through list
	for i in range(len(object_list)):
		for j in range(i+1, len(object_list)):
			curr = object_list[i]
			next = object_list[j]
	# for curr in object_list[0:len(object_list)-1]:
		# for next in object_list[1:len(object_list)]:
			pt1=curr.dorm_address.split(',')
			pt2=next.dorm_address.split(',')
			lat1=float(pt1[0])
			lon1=float(pt1[1])
			lat2=float(pt2[0])
			lon2=float(pt2[1])
			d[(curr.id,next.id)]=haversine(lon1,lat1,lon2,lat2)
	# print d

	# for each id go through all the tuples it is mentioned in
	for loc in object_list:
		print "loc: ", loc
		l=[]
		newlist=[]
		print "ID: ", loc.id
		for key in d.keys():
			#if the location id is in a key
			if loc.id in key:
				#print loc.id, key
				#save that key-value pair in a list
				l.append((key,d.get(key)))
		#sort the list
		l.sort(key=operator.itemgetter(1))
		#save the smallest 5 values in another list
		closest_five=l[:5]
		# print "closest_five: ", closest_five
		#then take the id from the tuple that does not match
		#loc.id, and turn those ids into a string
		for x in closest_five:
			# print x[0][0]
			if x[0][0]==loc.id:
				newlist.append(x[0][1])
			else:
				 newlist.append(x[0][0])
		#print "LIST OF IDS: ", newlist
		loc.closest_rooms = ",".join(map(str,newlist))
		print "FINAL STRING: ", loc.closest_rooms
		app.add_to_database(loc)
		print "committed"

#cd2() fixes cd()'s problem of no closest five for locations that don't have machines
def cd2():

	#get all the location ids that have machines
	machine_ids = model.session.query(model.Machine.location_id).group_by(model.Machine.location_id).all()
	#convert list of tuples into a list
	list_of_m_ids = [r for (r,) in machine_ids]
	print "machine ids: ", list_of_m_ids
	#get all location ids that exist
	ids = model.session.query(model.Location.id).all()
	list_of_ids = [r for (r,) in ids]
	print "all ids: ", list_of_ids
	
	m_object_list = []
	object_list = []
	#create Location objects for each id
	for i in list_of_m_ids:
		m_object_list.append(model.session.query(model.Location).filter_by(id=i).one())
	print "m_object_list: ", m_object_list
	print "length of m_object_list: ", len(m_object_list)

	for i in list_of_ids:
		object_list.append(model.session.query(model.Location).filter_by(id=i).one())
	print "object_list: ", object_list
	print "length of object_list: ", len(object_list)

	d={}
	for i in range(len(object_list)):
		for j in range(len(object_list)):
			curr = object_list[i]
			next = object_list[j]
			print "curr.id: ", curr.id
			print "next.id: ", next.id
			print "machines: ", next.machines
			if curr.id == next.id:
				continue
			if len(next.machines) > 0:
				pt1=curr.dorm_address.split(',')
				pt2=next.dorm_address.split(',')
				lat1=float(pt1[0])
				lon1=float(pt1[1])
				lat2=float(pt2[0])
				lon2=float(pt2[1])
				d[(curr.id,next.id)]=haversine(lon1,lat1,lon2,lat2)
			else: #the location B doesn't have any untis
				continue

	print "d: ", d

	for loc in object_list:
		print "loc: ", loc
		l=[]
		newlist=[]
		print "ID: ", loc.id
		for key in d.keys():
			if key[0] == loc.id:
				l.append((key[1],d.get(key)))
		#sort my list
		l.sort(key=operator.itemgetter(1))
		#save the smallest 5 values in another list
		closest_five=l[:5]
		for x in closest_five:
			newlist.append(x[0])
		loc.closest_rooms = ",".join(map(str,newlist))
		print "FINAL STRING: ", loc.closest_rooms	
		app.add_to_database(loc)
		print "committed"	


