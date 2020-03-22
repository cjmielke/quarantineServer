#!/usr/bin/python2.7
import argparse

from app.models import db
from app.models.tranches import Tranche

'''

This script scans a list of tranche URLs and populates the database tranche table

'''


#set up the flask app

parser = argparse.ArgumentParser()
parser.add_argument('-production', action='store_true')
args = parser.parse_args()

debug = True
if args.production: debug = False


'''
Physico-chemical property space in 3D is organized into 121 first-level tranches: size and polarity. Within each of these, we subdivide into a further four dimensions: reactivity, purchasability, pH and charge. This results in a six-dimensional space, as follows:

* First letter is the molecular weight bin - a measure of size - horizontal axis, left to right, online.
* Second letter is the logP bin - a measure of polarity - vertical axis, top to bottom, online.

Within each first-level tranche are four dimensional subdirectories, for a total of six dimensions.
Use the Tranche Browser to facilitate downloading these files. The Tranche Browser is thought to be 100,000 times faster than using /substances/subsets/for-sale, for instance.
* The third letter is reactivity : A=anodyne. B=Bother (e.g. chromophores) C=clean (but pains ok), E=mild reactivity ok, G=reactive ok, I = hot chemistry ok
* The fourth letter is purchasability: A and B = in stock, C = in stock via agent, D = make on demand, E = boutique (expensive), F=annotated (not for sale)
* The fifth letter is pH range: R = ref (7.4), M = mid (near 7.4), L = low (around 6.4), H=high (around 8.4).
* The sixth and last dimension is net molecular charge. Here we follow the convention of InChIkeys. Thus. N = neutral, M = minus 1, L = minus 2 (or greater). O = plus 1, P = plus 2 (or greater).
'''

#@click.command(name='db-init-data')
#@with_appcontext
def scan():
	"""Init db with some data"""

	from app.core import create_app

	app = create_app(debug=debug)

	with app.app_context():
		db.create_all()
		# your code here
		with open('ZINC-downloader-3D-pdbqt.gz.uri', 'r') as tracheList:
			for line in tracheList:
				line=line.rstrip()
				urlPath = line.replace('http://files.docking.org/', '')
				fileName = urlPath.split('/')[-1]

				print line, urlPath, fileName

				t = Tranche()
				t.urlPath = urlPath
				t.fileName = fileName

				t.lastAssigned=0
				t.loopCount=0
				t.ligandCount=None		# unknown until we figure it out

				t.weight = fileName[0]
				t.logP = fileName[1]
				t.reactivity = fileName[2]
				t.purchasibility = fileName[3]
				t.pH = fileName[4]
				t.charge = fileName[5]

				t.subset = '3D'			# "all"

				print t
				db.session.add(t)
			db.session.commit()	# faster out of loop


if __name__ == "__main__":
	scan()

