from flask import Flask, render_template, redirect, request, flash, session, g, url_for
from twilio.rest import TwilioRestClient
from sqlalchemy import distinct
import model
import datetime
import time
import re

app = Flask(__name__)

#testing ability to get signal from Twine
@app.route("/", methods=['GET','POST'])
def index():
	
	# return render_template("haversine.html")
	schools = model.session.query(model.Location).group_by(model.Location.school).all()	
	return render_template("homepage.html", schools=schools)

def add_to_database(letter):
	model.session.add(letter)
	model.session.commit()
	model.session.refresh(letter)

@app.route("/load_info")
def new_load():
	
	l = model.Load()
	#get machine id from sensor
	l.machine_id = request.args.get("id")
	print "machine id is: ", l.machine_id
	machine = model.session.query(model.Machine).filter_by(id=l.machine_id).one()
	add_to_database(l)
	
	#get machine status from sensor
	l.machine.in_use = request.args.get("vibration")	
	
	#remove the brackets that are from the senor's status request * #get a sub-string of a string instead
	l.machine.in_use = l.machine.in_use.replace('[','')
	l.machine.in_use = l.machine.in_use.replace(']','')
	add_to_database(machine)

	#creates two entries into loads table, one for start time and one for end time, 
	#i want just one entry with both start and end time could use update, but how to query for it?
	if l.machine.in_use == "shaking":
		l.start_time = datetime.datetime.today()
		print "start time is: ", l.start_time
		add_to_database(l)

	# else:
	# 	l.end_time = datetime.datetime.today()
	# 	print "end time is: ", l.end_time

	# add_to_database(l)

	print "machine_status is: ", l.machine.in_use
	print "machine: ", machine
	print "machine's location id: ", l.machine.location_id
	
	# Account Sid and Auth Token
	# account_sid = "AC66a7dc1fa19168fb9cf082c3f0cf8d30"
	# auth_token = ##add back in" "
	# client = TwilioRestClient(account_sid, auth_token)

	#*************
	# if l.machine.in_use == "shaking":
	# 	l.start_time = time.time()
	# 	#start_time = time.time()
	# 	#print "start_time: ", start_time
	# 	#convert start_time into datetime type
	# 	#l.start_time = datetime.datetime.fromtimestamp(start_time)
	# 	print "l.start_time: ", l.start_time
	# 	model.session.add(l)
	# 	model.session.commit()
	# 	model.session.refresh(l)
	#******************

	# if l.machine.type == "Washer":
	# 	#duration = 1800	#duration = 30mins or 1800secs
	# 	duration = 90
	# 	text_time = l.start_time + 45
	# 	if time.time() == text_time:
	# 		message = client.sms.messages.create(body="machine will be available in 45 seconds",
	# 											to="+5107898157",
	# 											from_="+15104021338")
	# 		print "MESSAGE: ", message.sid
	# else:
	# 	#duration = 3600
	# 	duration = 120
	# 	text_time = l.start_time + 60
	# 	if time.time() == text_time:
	# 		message = client.sms.messages.create(body="machine will be available in 1 minute",
	# 											to="+5107898157",
	# 											from_="+15104021338")
	# 		print "MESSAGE: ", message.sid



	###################
	#this will all be specific to a machine, right?......

	#what i want to do, store a start time for a machine
	#when i get a "still" message for that same machine, store
	#the end time.

	# if l.machine.in_use == "shaking":
	# 	l.start_time = time.time()
	# 	print "start_time in seconds: ", l.start_time
	# 	print "actual start time: ", datetime.datetime.fromtimestamp(l.start_time).strftime('%Y-%m-%d %H:%M:%S')

	# else:
	# 	l.end_time = time.time()
	# 	print "end_time in seconds: ", l.end_time
	# 	print "actual end time: ", datetime.datetime.fromtimestamp(l.end_time).strftime('%Y-%m-%d %H:%M:%S')

	# try: 
	# 	duration = l.end_time - l.start_time
	# 	print "duration is: ", duration
	# 	print "actual duration is: ", datetime.datetime.fromtimestamp(duration).strftime('%Y-%m-%d %H:%M:%S')
	# except TypeError:
	# 	print "no end time"
	
	# model.session.add(l)
	# model.session.commit()

	
	location = model.session.query(model.Location).filter_by(id=l.machine.location_id).one()
	print "specific location: ", l.machine.location.school,l.machine.location.dorm,l.machine.location.floor
	
	#get all the machines at the specified location id
	all_machines = model.session.query(model.Machine).filter_by(location_id=l.machine.location_id).all()
	print "all_machines: ", all_machines

	#replace the spaces in school or dorm names with a underscore in order to call appropriate template
	underscore_school = l.machine.location.school.replace(' ', '_')
	underscore_dorm = l.machine.location.dorm.replace(' ', '_')

	return render_template("%s%s.html" %(underscore_school,underscore_dorm),load=l,machines=all_machines) 
	
	#************************************************************************
	#for now, I'm going to assume the layout of the laundry room on each floor is the same within a dorm

@app.route("/get_dorms", methods=["POST"])
def get_dorm():

	school = request.form['school']
	#get all the dorms that correspond to that dorm
	dorms = model.session.query(model.Location.dorm).filter_by(school=school).group_by(model.Location.dorm).all()	
	return render_template("enter_dorm.html", dorms = dorms, school = school)

	# schools = model.session.query(model.Location).filter(model.Location.school.like("%" + school + "%")).group_by(model.Location.school).all()
	
	# if not schools:
	# 	flash("Sorry, we do not provide service for your school yet")
	# 	return redirect("/")
	
	# return render_template("enter_dorm.html", schools = schools)

@app.route("/get_floors", methods=["POST"])
def get_floors():

	dorm = request.form['dorm']
	school = request.form['school']
	floors = model.session.query(model.Location.floor).filter_by(dorm=dorm).group_by(model.Location.floor).all()
	return render_template("enter_floor.html", floors=floors, dorm = dorm, school = school)

@app.route("/room_layout", methods=["GET","POST"])
def room_layout():

	floor = request.values['floor']
	school = request.values['school']
	dorm = request.values['dorm']
	
	#query for location id that matches the school, dorm, floor
	###how to do this for VCW because it doesn't have a laundry machine??
	location = model.session.query(model.Location).filter_by(school=school,dorm=dorm,floor=floor).first()
	print "location: ", location
	all_machines = model.session.query(model.Machine).filter_by(location_id=location.id).all()
	print "all_machines: ", all_machines
	#replace the spaces in school & dorm names with an underscore to call appropriate template
	underscore_school = school.replace(' ', '_')
	underscore_dorm = dorm.replace(' ', '_')

	#need to do test cases for dorms that don't have an html pg because there are no 
	#laundry rooms. want to just show them the closest laundry rooms to them

	#make list of closest rooms' ids
	room_list = location.closest_rooms.split(",")
	print "room_list: ", room_list
	#make the elements of the list integers
	room_list = [int(i) for i in room_list]
	print "room_list ints: ", room_list
	#search for laundry objects whose id matches with the ids of the closest rooms
	#add results to a list called "rooms"
	rooms = []
	for rm_id in room_list:
		rooms.append(model.session.query(model.Location).filter_by(id=rm_id).one())
	print "list of room objects: ", rooms

	return render_template("%s%s.html" %(underscore_school,underscore_dorm), location=location, machines=all_machines, rooms=rooms) 

app.secret_key="""oiueorijwr902irkjklak"""
	
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
	