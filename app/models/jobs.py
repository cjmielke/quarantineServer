import datetime


from . import db


class Job(db.Model):

	__tablename__ = 'jobs'

	id = db.Column('jobID', db.Integer, primary_key = True)

	zincID = db.Column('zincID', db.Integer)
	ipAddr = db.Column('ip', db.Integer)

	timeCreated = db.Column('timeCreated', db.DateTime, default=datetime.datetime.utcnow)
	timeFinished = db.Column('timeFinished', db.DateTime, default=None)

	dob = db.Column(db.DateTime)



def getJob(id):
	job = Job.query.get(int(id))
	return job
