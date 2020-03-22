import datetime


from . import db

class User(db.Model):

	__tablename__ = 'users'
	user = db.Column('user', db.Integer, primary_key = True)
	username = db.Column('username', db.String(16))

'''
DB=db
class EntityModel(DB.Model):
	id = DB.Column(DB.Unicode(37), primary_key=True)

class DocumentModel(DB.Model):
	id = DB.Column(DB.Unicode(37), primary_key=True)
	entity_id = DB.Column(DB.Unicode(37), DB.ForeignKey('entity.id',   ondelete='cascade'), nullable=True)
	entity = DB.relationship('EntityModel')
'''

class Job(db.Model):

	__tablename__ = 'jobs'

	id = db.Column('jobID', db.Integer, primary_key = True)
	#user = db.Column('user', db.String(16))
	user = db.Column('user', db.ForeignKey('users.user'), nullable=True, index=True)
	#userID = db.Column('user', db.Integer)

	zincID = db.Column('zincID', db.Integer)
	receptor = db.Column('receptor', db.String(16))
	ipAddr = db.Column('ip', db.Integer)

	bestDG = db.Column('bestDG', db.Float, index=True)
	bestKi = db.Column('bestKi', db.Float)

	algo = db.Column('algo', db.String(12))		# AD, AD-gpu, AD-vina

	time = db.Column('time', db.Integer)

	timestamp = db.Column('timestamp', db.DateTime, default=datetime.datetime.utcnow)


def getJob(id):
	job = Job.query.get(int(id))
	return job


def testModels():



	u = User()
	u.username = 'testUser'
	db.session.add(u)
	db.session.commit()

	j = Job()
	j.user = u.user
	j.bestDG = -7
	j.zincID = 10

	db.session.add(j)
	db.session.commit()


