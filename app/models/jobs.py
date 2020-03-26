import datetime


from . import db

class User(db.Model):

	__tablename__ = 'users'
	user = db.Column('user', db.Integer, primary_key = True)
	username = db.Column('username', db.String(16))


class Job(db.Model):

	__tablename__ = 'jobs'

	id = db.Column('jobID', db.Integer, primary_key = True)
	#user = db.Column('user', db.String(16))
	#user = db.Column('user', db.ForeignKey('users.user'), nullable=True, index=True)
	user = db.Column('user', db.Integer, index=True)

	trancheID = db.Column('trancheID', db.Integer)
	trancheLigand = db.Column('trancheLigand', db.Integer)

	zincID = db.Column('zincID', db.Integer)
	receptor = db.Column('receptor', db.String(16))
	ipAddr = db.Column('ip', db.Integer)

	bestDG = db.Column('bestDG', db.Float, index=True)
	bestKi = db.Column('bestKi', db.Float)

	algo = db.Column('algo', db.String(12))		# AD, AD-gpu, AD-vina

	time = db.Column('time', db.Integer)

	timestamp = db.Column('timestamp', db.DateTime, default=datetime.datetime.utcnow)

	uploaded = db.Column('uploaded', db.Boolean, index=True)


def getJob(id):
	# type: (int) -> Job
	job = Job.query.get(int(id))
	return job


def testModels():

	test_user = 'testUser'

	user = User.query.filter(User.username == test_user).first()
	print user
	if not user:
		user = User()
		user.username = test_user
		db.session.add(user)
		db.session.commit()

	j = Job()
	j.user = user.user
	j.bestDG = -7
	j.zincID = 10

	db.session.add(j)
	db.session.commit()


