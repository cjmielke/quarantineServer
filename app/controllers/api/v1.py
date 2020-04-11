from __future__ import unicode_literals

import json
import os
import random

from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import text
from werkzeug.datastructures import FileStorage

from app.controllers import add_blueprint
from app.initializers.settings import LIVE_RECEPTORS, ALL_RECEPTORS, LOCAL_ZINC, RESULTS_STORAGE, DOCKING_ALGOS
from app.models import db

#from app.controllers.api import bp
from app.models.tranches import getTranche
from app.util import safer

bp = Blueprint('apiv1', __name__, url_prefix='/api/v1')

from app.models.jobs import Job, User


# FIXME - Make a homepage later .... with a table of best results
@bp.route('/')
def index():
	return render_template('home/welcome.html.jade')



'''

First letter is the molecular weight bin - a measure of size - horizontal axis, left to right, online.
Second letter is the logP bin - a measure of polarity - vertical axis, top to bottom, online.

Within each first-level tranche are four dimensional subdirectories, for a total of six dimensions.
Use the Tranche Browser to facilitate downloading these files. The Tranche Browser is thought to be 100,000 times faster than using /substances/subsets/for-sale, for instance.
	The third letter is reactivity : A=anodyne. B=Bother (e.g. chromophores) C=clean (but pains ok), E=mild reactivity ok, G=reactive ok, I = hot chemistry ok
	The fourth letter is purchasability: A and B = in stock, C = in stock via agent, D = make on demand, E = boutique (expensive), F=annotated (not for sale)
	The fifth letter is pH range: R = ref (7.4), M = mid (near 7.4), L = low (around 6.4), H=high (around 8.4).
	The sixth and last dimension is net molecular charge. Here we follow the convention of InChIkeys. Thus. N = neutral, M = minus 1, L = minus 2 (or greater). O = plus 1, P = plus 2 (or greater).

'''

'''
# tranches defined in this case by individual compressed pdbqt.gz files
tranches = [
	'BAAAML.xaa.pdbqt.gz',
	'BBAAML.xaa.pdbqt.gz',
	'BCAAML.xaa.pdbqt.gz'
]

class Tranche():
	def __init__(self, trancheName):
		self.name = trancheName
		self.lastModel = 0
		return

	def nextModel(self):
		self.lastModel+=1
		return self.lastModel


class TrancheModels():

	def __init__(self):
		self.tranches = {}
		return

	def nextModel(self, trancheName):
		if trancheName not in self.tranches:
			# look in database to find the most recently completed modelID
			# not in database? Then set modelNum = 0
			self.tranches[trancheName] = Tranche(trancheName)
			pass
		tr = self.tranches[trancheName]
		return tr.nextModel()


assigner = TrancheModels()			# single object shared among all threads
'''




@bp.route('/tranche/get')
def assignTranche():
	'''
	Picks a random tranche file, and reports back to client
	Client will then download this file, and for the duration of its runtime process ligands from it until exhaustion
	This minimizes bandwidth usage on the ZINC server, or any mirrors that may be created
	'''
	#rt = random.choice(tranches)

	#'ABCDEFGHIJK'
	weights = "'A','B','C','D','E','F','G','H','I','J','K'"
	logPs = "'A','B','C','D','E','F','G','H','I','J','K'"

	'''
	The third letter is reactivity : A=anodyne. B=Bother (e.g. chromophores) C=clean (but pains ok), E=mild reactivity ok, G=reactive ok, I = hot chemistry ok
	The fourth letter is purchasability: A and B = in stock, C = in stock via agent, D = make on demand, E = boutique (expensive), F=annotated (not for sale)
	The fifth letter is pH range: R = ref (7.4), M = mid (near 7.4), L = low (around 6.4), H=high (around 8.4).
	The sixth and last dimension is net molecular charge. Here we follow the convention of InChIkeys. Thus. N = neutral, M = minus 1, L = minus 2 (or greater). O = plus 1, P = plus 2 (or greater).
	'''

	reactivity = 'ABCEGI'
	purch = 'ABCDEF'

	query = text('''
		SELECT * from tranches
		WHERE weight in ('A','B','C','D','E','F','G','H','I','J','K')
		AND logP in ('A')
		AND purchasibility in ('A','B')
		AND pH in ('R','M')
		AND charge in ('N','M','O');
	''')

	query = text('''
		SELECT * from tranches
		WHERE weight in ('A','B','C','D','E','F','G','H','I','J','K')
		AND purchasibility in ('A','B')
		AND pH in ('R','M')
		AND charge in ('N','M','O')
		AND loopCount<5
		;
	''')

	rows = db.engine.execute(query)
	rows = [r for r in rows]
	print 'tranches selected : ', len(rows)
	selection = random.choice(rows)

	response = dict(tranche=selection.urlPath, id=selection.trancheID)

	# does the server have a local cached copy?
	localPath = os.path.join(LOCAL_ZINC, selection.urlPath)
	if os.path.exists(localPath):
		response['mirror'] = 'https://quarantine.infino.me/ligands/'

	return jsonify(**response)


@bp.route('/tranches/<int:trancheID>/nextligand')
def getTrancheJob(trancheID):
	'''
	Get the most recent model number assigned for this tranche, and increment it. Assign this to the client
	the client will then spool through the tranche file looking for this model number, and take the next one
	'''
	#nm = assigner.nextModel(tranche)

	tranche = getTranche(trancheID)
	print tranche.lastAssigned
	tranche.lastAssigned += 1

	db.session.commit()
	#receptors = ['spike-1', 'mpro-1']				# hardcoded for now - future versions of API will assess what's needed from database
	#receptors = ['mpro-1']
	receptors = LIVE_RECEPTORS

	return jsonify(**dict(ligand=tranche.lastAssigned, receptors=receptors))

@bp.route('/tranches/<int:trancheID>/out')
def TrancheEOF(trancheID):
	tranche = getTranche(trancheID)
	print tranche.lastAssigned
	tranche.lastAssigned -= 1
	tranche.loopCount += 1
	db.session.commit()
	return jsonify(**dict(status='ok'))


from ipaddress import ip_address


@bp.route('/submitresults', methods=['GET','POST'])
def submitResults():

	#if request.method == 'GET':
	#	return render_template('results.html.jade')

	if request.method == 'POST':

		if request.is_json:
			logFile = None
			content = request.get_json()
		else:
			content = json.load(request.files['data'])

		print (content)
		print request.remote_addr

		ip = ip_address(unicode(request.remote_addr))
		print request.files

		userName = content.get('user', None)
		if userName: userName = safer(userName)

		user = User.query.filter(User.username == userName).first()
		if not user:
			user = User()
			user.username = userName
			db.session.add(user)
			db.session.commit()

		j = Job()

		#assert content['zincID'].startswith('ZINC')
		j.user = user.user

		j.trancheID = int(content['tranche'])
		j.trancheLigand = int(content['ligand'])

		j.zincID = int(content['zincID'].replace('ZINC',''))

		receptor = content['receptor']
		if receptor not in ALL_RECEPTORS:
			raise ValueError('invalid receptor reported!')

		j.receptor = receptor
		j.ipAddr = int(ip)                         # not working since uwsgi deployment!
		j.bestDG = float(content['bestDG'])

		bestKi = content.get('bestKi', None)
		if bestKi is not None: bestKi=float(bestKi)
		j.bestKi = bestKi

		algo = content['algo']
		assert algo in DOCKING_ALGOS
		j.algo = algo

		j.time = int(content['time'])

		if 'test' not in content:
			db.session.add(j)
			db.session.commit()

		if 'logfile' in request.files:
			logFile = request.files['logfile']  # type: FileStorage
			savePath = os.path.join(RESULTS_STORAGE, '%s.dlg.gz' % j.id)
			logFile.save(savePath)


		return jsonify(**dict(status='thanks', id=j.id))


add_blueprint(bp)


