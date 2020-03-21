import datetime


from . import db


class Job(db.Model):

	__tablename__ = 'jobs'

	id = db.Column('jobID', db.Integer, primary_key = True)

	zincID = db.Column('zincID', db.Integer)
	receptor = db.Column('receptor', db.String(16))
	ipAddr = db.Column('ip', db.Integer)

	bestDG = db.Column('bestDG', db.Float)
	bestKi = db.Column('bestKi', db.Float)

	algo = db.Column('algo', db.String(12))		# AD, AD-gpu, AD-vina

	time = db.Column('time', db.Integer)

	timestamp = db.Column('timestamp', db.DateTime, default=datetime.datetime.utcnow)


def getJob(id):
	job = Job.query.get(int(id))
	return job
