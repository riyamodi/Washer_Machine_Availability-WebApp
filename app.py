from flask import Flask, render_template, redirect, request, flash, session, g, url_for
from twilio.rest import TwilioRestClient
from sqlalchemy import distinct
from datetime import datetime, timedelta
import model
import floor_text
#import datetime
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
	
	add_to_database(machine)

	print "machine_status is: ", l.machine.in_use
	print "machine: ", machine
	print "machine's location id: ", l.machine.location_id

	if l.machine.in_use == "shaking":
		l.start_time = datetime.today()
		print "start time is: ", l.start_time
		if l.machine.type == "Washer":
			l.end_time = l.start_time + timedelta(seconds=60)
		if l.machine.type == "Dryer":
			l.end_time = l.start_time + timedelta(seconds=90)
		print "end time is: ", l.end_time
		add_to_database(l)

	return "committed new load!!"

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
	#!!! ONCE i get closest rooms for all places, then i will delete this if statement code
	if not all_machines:
		print "THIS IS WHAT WAS TRIGGERED"
		return render_template("%s%s.html" %(underscore_school,underscore_dorm), location=location, machines=all_machines) 

	#make list of closest rooms' ids
	room_list = location.closest_rooms.split(",")
	print "room_list: ", room_list
	#make the elements of the list integers
	room_list = [int(i) for i in room_list]
	print "room_list ints: ", room_list
	#search for laundry objects whose id matches with the ids of the closest rooms add results to a list called "rooms"
	rooms = []
	for rm_id in room_list:
		rooms.append(model.session.query(model.Location).filter_by(id=rm_id).one())
	print "list of room objects: ", rooms

	return render_template("%s%s.html" %(underscore_school,underscore_dorm), location=location, machines=all_machines, rooms=rooms) 

@app.route("/send_text", methods=["GET","POST"])
def send_text():
	print "in function"
	
	floor = request.values['floor']
	school = request.values['school']
	dorm = request.values['dorm']
	machine_type = request.values['type']

	print "DID THIS PRINT: ", school, dorm, floor, machine_type

	#get the location (id)
	location = model.session.query(model.Location).filter_by(school=school,dorm=dorm,floor=floor).one()
	print "location.id: ", location.id

	notification = model.Waiting_List()
	print "notification: ", notification
	#set notification location id column
	notification.location_id = location.id
	print "notification.location_id: ", notification.location_id
	notification.machine_type = machine_type
	print "notification.machine_type: ", notification.machine_type
	#add info to the database
	add_to_database(notification)
	print "added notification request to database"

	flash("Request recorded")

	return redirect ("/room_layout?school=%s&dorm=%s&floor=%s" %(school,dorm,floor))
	#return render_template("%s%s.html" %(underscore_school,underscore_dorm), location=location, machines=all_machines, rooms=rooms) 


app.secret_key="""oiueorijwr902irkjklak"""
	
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
	