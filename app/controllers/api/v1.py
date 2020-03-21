from __future__ import unicode_literals

import random

from flask import Blueprint, render_template, request, jsonify

from app.controllers import add_blueprint
from app.models import db

#from app.controllers.api import bp
bp = Blueprint('apiv1', __name__, url_prefix='/api/v1')

from app.models.jobs import Job




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



@bp.route('/tranche/get')
def getTranche():
	'''
	Picks a random tranche file, and reports back to client
	Client will then download this file, and for the duration of its runtime process ligands from it until exhaustion
	This minimizes bandwidth usage on the ZINC server, or any mirrors that may be created
	'''
	rt = random.choice(tranches)
	return jsonify(**dict(tranche=rt))


@bp.route('/tranches/<tranche>/nextligand')
def getTrancheJob(tranche):
	'''
	Get the most recent model number assigned for this tranche, and increment it. Assign this to the client
	the client will then spool through the tranche file looking for this model number, and take the next one
	'''
	nm = assigner.nextModel(tranche)

	#receptors = ['spike-1', 'mpro-1']				# hardcoded for now - future versions of API will assess what's needed from database
	receptors = ['mpro-1']

	return jsonify(**dict(ligand=nm, receptors=receptors))



from ipaddress import ip_address


@bp.route('/submitresults', methods=['GET','POST'])
def submitResults():

	if request.method == 'GET':
		return render_template('results.html.jade')

	elif request.method == 'POST':

		print (request.is_json)
		content = request.get_json()
		print (content)
		print request.remote_addr

		ip = ip_address(unicode(request.remote_addr))
		print ip, int(ip)

		j = Job()

		#assert content['zincID'].startswith('ZINC')
		j.zincID = int(content['zincID'].replace('ZINC',''))
		j.receptor = content['receptor']
		j.ipAddr = int(ip)
		j.bestDG = float(content['bestDG'])

		bestKi = content.get('bestKi', None)
		if bestKi is not None: bestKi=float(bestKi)
		j.bestKi = bestKi

		algo = content['algo']
		assert algo in ['AD4', 'AD-gpu', 'AD-vina']
		j.algo = algo

		j.time = int(content['time'])


		if 'test' not in content:
			db.session.add(j)
			db.session.commit()

		return jsonify(**{'status': 'thanks'})


add_blueprint(bp)


