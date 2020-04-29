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


def random3DTranche():
	weights = "'A','B','C','D','E','F','G','H','I','J','K'"
	logPs = "'A','B','C','D','E','F','G','H','I','J','K'"

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

	# these are ordered by liklihood that they will have an FDA ligand
	query = text('''
		SELECT * from tranches
		WHERE weight in ('C','A','B','K','D','G','H')
		AND logP in ('D','K','E','F','C','G', 'I', 'H', 'B', 'A', 'J')
		AND purchasibility in ('A','B','E')
		AND pH in ('R','M')
		AND charge in ('N','O','M');
	''')


	# NOTE - no limitation whatsoever on logP - only really limiting purchasibility, pH, and extreme charge states
	query = text('''
		SELECT * from tranches
		WHERE weight in ('A','B','C','D','E','F','G','H','I','J','K')
		AND reactivity in ('A', 'E')
		AND purchasibility in ('A','B')
		AND pH in ('R','M')
		AND charge in ('N','M','O')
		ORDER BY loopCount asc
		LIMIT 100
		;
	''')

	rows = db.engine.execute(query)
	rows = [r for r in rows]

	return rows



def specialWeighted3DTranches():
	'''Pulls tranches from the global 3D set, but preferrentially grabs tranches with the most FDA-cleared drugs'''

	# NOTE - no limitation whatsoever on logP - only really limiting purchasibility, pH, and extreme charge states
	query = text('''
		select * from tranches
		join FDATranches using(trancheName)
		order by loopCount asc, numDrugs desc
		LIMIT 1
	;''')

	rows = db.engine.execute(query)
	rows = [r for r in rows]

	return rows



def randomSubsetTranche(subset):

	query = text('''
		SELECT * from tranches
		WHERE subset=:subset
	''')

	rows = db.engine.execute(query, subset=subset)
	rows = [r for r in rows]

	return rows


def customTranche():
	query = text('SELECT * from tranches WHERE subset="custom" ORDER BY loopCount asc LIMIT 1;')
	rows = db.engine.execute(query)
	rows = [r for r in rows]
	return rows


@bp.route('/tranche/get')
def assignTranche():
	'''
	Picks a random tranche file, and reports back to client
	Client will then download this file, and for the duration of its runtime process ligands from it until exhaustion
	This minimizes bandwidth usage on the ZINC server, or any mirrors that may be created
	'''
	#rt = random.choice(tranches)

	#'ABCDEFGHIJK'

	rows = random3DTranche()

	rows = [r for r in rows]
	selection = random.choice(rows)

	response = dict(tranche=selection.urlPath, id=selection.trancheID)

	# disabling mirror support for now   - this wasn't even the right implementation!
	# does the server have a local cached copy?
	#localPath = os.path.join(LOCAL_ZINC, selection.urlPath)
	#if os.path.exists(localPath):
	#	response['mirror'] = 'https://quarantine.infino.me/ligands/'

	return jsonify(**response)

# testing here for now
@bp.route('/tranche/getspecial')
def assignTrancheSpecial():

	# disabled moonshots for now
	if random.random() < 0.2:                       # moonshot - pull from the "everything" subset
		rows = specialWeighted3DTranches()
		if len(rows)==0:
			rows = random3DTranche()
	else:                                           # pick instead from annotated subsets, fda cleared, etc
		# FIXME - these don't work sadly .... the special subsets on files.docking.org seem corrupt :/
		#subset = random.choice(['fda', 'world', 'in-vivo'])     # something seriously wrong with special subsets on zincDB
		#subset = random.choice(['fda'])
		#rows = randomSubsetTranche(subset)

		rows = customTranche()
		if len(rows)==0:
			rows = random3DTranche()


	selection = random.choice(rows)

	resp = dict(tranche=selection.urlPath, id=selection.trancheID)
	if 'custom' in selection.urlPath: resp['mirror'] = 'https://quarantine.infino.me/ligands/'
	response = resp

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
	receptors = LIVE_RECEPTORS

	return jsonify(**dict(ligand=tranche.lastAssigned, receptors=receptors))

@bp.route('/tranches/<int:trancheID>/out')
def TrancheEOF(trancheID):
	tranche = getTranche(trancheID)
	print tranche.lastAssigned
	#tranche.lastAssigned -= 1
	tranche.lastAssigned = 0        # really should just reset from now on, especially with smaller subsets!
	if tranche.loopCount is None: tranche.loopCount=0   # this killed me ...
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


