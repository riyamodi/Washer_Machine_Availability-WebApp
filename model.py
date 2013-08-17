from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///laundry.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit=False,autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

#Class declarations

class Machine(Base):

	__tablename__ = "machines"

	id = Column(Integer, primary_key = True)
	type = Column(String(64))
	in_use = Column(String(64))		
	location_id = Column(Integer, ForeignKey('locations.id'))

	location = relationship("Location",backref=backref("machines",order_by=id))
	#waiting_list = relationship("Waiting_List",backref=backref("machines",order_by=id))

class Load(Base):
	__tablename__ = "loads"

	id = Column(Integer, primary_key = True)
	machine_id = Column(Integer, ForeignKey('machines.id'))
	start_time = Column(DateTime, nullable = True) 	
	end_time = Column(DateTime, nullable = True)
	user_id = Column(Integer, ForeignKey('users.id'),nullable=True)
	
	machine = relationship("Machine",backref=backref("load",order_by=id))
	user = relationship("User",backref=backref("load",order_by=id))

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	location_id = Column(Integer, ForeignKey('locations.id'))
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)
	cellphone_num = Column(String(64), nullable = True)

	waiting_list = relationship("Waiting_List",backref=backref("users",order_by=id))
	location = relationship("Location",backref=backref("users",order_by=id))

class Location(Base):
	__tablename__ = "locations"

	id = Column(Integer, primary_key = True)
	school = Column(String(64))
	dorm = Column(String(64))
	dorm_address = Column(String(64), nullable = True)
	floor = Column(Integer)
	closest_rooms = Column(String(64), nullable = True)

class Waiting_List(Base):	
	__tablename__ = "waiting_list"

	id = Column(Integer, primary_key = True)
	location_id = Column(Integer, ForeignKey('locations.id'))
	machine_type = Column(Integer, ForeignKey('machines.type'),nullable = True)
	#machine_id = Column(Integer, ForeignKey ('machines.id'),nullable = True)
	user_id = Column(Integer, ForeignKey('users.id'),nullable = True)

	location = relationship("Location",backref=backref("waiting_list",order_by=id))
	

