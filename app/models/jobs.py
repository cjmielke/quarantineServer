import datetime

from app.core import app
from . import db

class User(db.Model):

	__tablename__ = 'users'
	user = db.Column('user', db.Integer, primary_key = True)
	username = db.Column('username', db.String(16))



# if encrypting the userID is desired, here is a clean way to do it with Blowfish


from Crypto.Cipher import Blowfish
from Crypto.Util.number import bytes_to_long, long_to_bytes


if app.debug:
	from app.initializers.settings import BLOWFISH_KEY
	print 'DEV MODE - USING FAKE BLOWFISH KEY'
else:
	from app.initializers.secrets import BLOWFISH_KEY

c1  = Blowfish.new(BLOWFISH_KEY, Blowfish.MODE_ECB)



# the following work on long integer representations of IPv4 addresses

def encryptIP(ipInt):
	enc = bytes_to_long(c1.encrypt(long_to_bytes(ipInt, blocksize=8)))
	return enc

def decryptIP(enc):
	dec=bytes_to_long(c1.decrypt(long_to_bytes(enc, blocksize=8)))
	return dec




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


'''
This is a table that holds records of processed logfiles - which will be a small subset of all jobs
Could store one row per ligand pose .....
'''
# FIXME - On second thought, I feel like just adding a 'haveLog' column to the Jobs table for now
class Result(db.Model):

	__tablename__ = 'results'

	id = db.Column('jobID', db.Integer, primary_key = True)
	pose = db.Column('pose', db.Integer, primary_key = True)

	energy = db.Column('energy', db.Float, index=True)


