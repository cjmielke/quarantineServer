import datetime


from . import db


class Tranche(db.Model):

	__tablename__ = 'tranches'

	id = db.Column('trancheID', db.Integer, primary_key = True)
	urlPath = db.Column('urlPath', db.String(128), unique = True, index=True)			# full path on files.docking.org where pdbqt is found

	fileName = db.Column('fileName', db.String(32), unique = True, index=True)			# full path on files.docking.org where pdbqt is found
	subset = db.Column('subset', db.String(16), index=True)			# full path on files.docking.org where pdbqt is found


	lastAssigned = db.Column('lastAssigned', db.Integer, index=True)

	# will be unknown by default until either server parses it or a user reports back
	# Im trusting clients for now, but down the road we'll do this more authoritatively
	ligandCount = db.Column('ligandCount', db.Integer, index=True)

	# count the number of times clients have reported reaching EOF
	loopCount = db.Column('loopCount', db.Integer, index=True)

	weight = db.Column('weight', db.String(1), index=True)
	logP = db.Column('logP', db.String(1), index=True)
	reactivity = db.Column('reactivity', db.String(1), index=True)
	purchasibility = db.Column('purchasibility', db.String(1), index=True)
	pH = db.Column('pH', db.String(1), index=True)
	charge = db.Column('charge', db.String(1), index=True)

	local = db.Column('local', db.Integer, index=True)


def getTranche(id):
	# type: (int) -> Tranche
	tranche = Tranche.query.get(int(id))
	return tranche



def testModels():

	db.session.commit()


