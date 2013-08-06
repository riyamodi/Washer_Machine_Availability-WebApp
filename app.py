from flask import Flask, render_template, redirect, request, flash, session, g, url_for
import model
import datetime
import re

app = Flask(__name__)

#testing ability to get signal from Twine
@app.route("/", methods=['GET','POST'])
def index():
	# print "at beggining of function"

	# vibration_status=request.form["vibration"]
	# print "vibration_status is", vibration_status

	# return "did it work?"

	return render_template("homepage.html")

@app.route("/load_info")
def new_load():
	
	l = model.Load()
	l.machine_id = request.args.get("id")
	print "machine id is: ", l.machine_id
	machine = model.session.query(model.Machine).filter_by(id=l.machine_id).one()
	model.session.add(l)
	model.session.commit()
	model.session.refresh(l)
	#############
	#do i need to commit the following line to session??
	l.machine.in_use = request.args.get("vibration")
	#should be a better way of doing this
	l.machine.in_use = l.machine.in_use.replace('[','')
	l.machine.in_use = l.machine.in_use.replace(']','')
	print "machine_status is: ", l.machine.in_use
	print "machine: ", machine
	print "machine's location id: ", l.machine.location_id
	location = model.session.query(model.Location).filter_by(id=l.machine.location_id).one()
	print "location: ", location
	print "specific location: ", l.machine.location.school,l.machine.location.dorm,l.machine.location.floor
	all_machines = model.session.query(model.Machine).filter_by(location_id=l.machine.location_id).all()
	print "all_machines: ", all_machines

	
	#I want the html template that I return to have variables within the html name
	#ex: [l.machine.location.school+l.machine.location.dorm+l.machine.location.floor].html
	#would be equivalent to: Georgetown_UniversityNew_South1.html
	#currently, school/dorm names longer than one word are separated by a space
	#in my database, so I want to rewrite it so spaces are replaced with underscores
	 
	underscore_school = l.machine.location.school.replace(' ', '_')
	print "new school: ", underscore_school
	underscore_dorm = l.machine.location.dorm.replace(' ', '_')
	print "new dorm: ", underscore_dorm

	return render_template("%s%s%d.html" %(underscore_school,underscore_dorm,l.machine.location.floor), 
							load=l,machines=all_machines)

	#****if it sends a request every second taht it is vibrating,
	#i need a way of only counting the first one
	# print "machine type: ", type(machine)
	# print "l.machine_id.machine type", type(l.machine_id.machine )
	# print "l.machine", type(l.machine)


	#MVP: get status, get id. find location id. display the room.
	


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
