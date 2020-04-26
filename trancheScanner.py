#!/usr/bin/python2.7
import argparse
import gzip
import os
import sys

from sqlalchemy import text

from app.initializers.settings import LOCAL_ZINC
from app.models import db
from app.models.tranches import Tranche, getTranche
from quarantineAtHome.getjob import TrancheReader

'''

This script scans a list of tranche URLs and populates the database tranche table

'''


#set up the flask app

parser = argparse.ArgumentParser()
parser.add_argument('-production', action='store_true')
parser.add_argument('-scan', action='store_true')
parser.add_argument('-load', action='store_true')
parser.add_argument('-special', action='store_true')
parser.add_argument('-fetch', action='store_true')
parser.add_argument('-build', type=str)
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


'''
ZINC-downloader-3D-pdbqt.gz.uri    file looks like this 
......
http://files.docking.org/3D/AA/AAMM/AAAAMM.xaa.pdbqt.gz
http://files.docking.org/3D/AA/AAMN/AAAAMN.xaa.pdbqt.gz
http://files.docking.org/3D/AA/AAMO/AAAAMO.xaa.pdbqt.gz
http://files.docking.org/3D/AA/AAMP/AAAAMP.xaa.pdbqt.gz
'''



def load3DTranches():
	""" Init db with information on tranches - tested with full 3D set only """

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


def loadSpecialTranches():
	"""
	decided to make this a seperate method to avoid making a mistake on production DB

	This was a cheap way to convert wget-d zincDB special directories :p

	find files.docking.org/special/ | grep pdbqt.gz > ~/specialTranches.txt
	 ....
	files.docking.org/special/current/fda/tranches/AJ/xaaa-AJ.ref.pdbqt.gz
	files.docking.org/special/current/fda/tranches/AJ/xaaa-AJ.mid.pdbqt.gz
	files.docking.org/special/current/fda/tranches/AB/xaaa-AB.ref.pdbqt.gz
	files.docking.org/special/current/fda/tranches/AB/xaaa-AB.mid.pdbqt.gz

	"""

	from app.core import create_app

	app = create_app(debug=debug)

	with app.app_context():
		db.create_all()

		with open('specialTranches.txt', 'r') as tracheList:
			for line in tracheList:
				assert 'special' in line

				line=line.rstrip()
				urlPath = line.replace('files.docking.org/', '')        # no http:// as before in the 3D tranche importer

				dirs = urlPath.split('/')
				fileName = dirs[-1]

				print line, urlPath, fileName

				assert dirs[0]=='special'
				# skipping dirs[1] which is usually 'current'
				subset = dirs[2]
				assert subset != '3D'

				t = Tranche()
				t.urlPath = urlPath
				t.fileName = fileName

				t.lastAssigned=0
				t.loopCount=0
				t.ligandCount=None		# unknown until we figure it out

				# not true anymore
				#t.weight = fileName[0]
				#t.logP = fileName[1]
				#t.reactivity = fileName[2]
				#t.purchasibility = fileName[3]
				#t.pH = fileName[4]
				#t.charge = fileName[5]

				# the first two tranche divisons appear to be stored in the last subdir
				weightLogP = dirs[-2]
				t.weight = weightLogP[0]
				t.logP = weightLogP[1]

				t.subset = subset



				print t
				db.session.add(t)
			db.session.commit()	# faster out of loop


def findLocalTranches():
	'''
	This finds tranche files on the webserver and marks them as being available for alternate download
	We don't need this yet, unless ZINC gets overloaded and wants us to offload bandwidth
	'''
	from app.core import create_app

	app = create_app(debug=debug)

	with app.app_context():

		print 'looking for cached ligand tranches'
		query = text('''
			SELECT * from tranches
		''')
		rows = db.engine.execute(query)
		# rows = [r for r in rows]

		for row in rows:
			print row.urlPath
			localPath = os.path.join(LOCAL_ZINC, row.urlPath)
			if os.path.exists(localPath):
				print 'Found! ', localPath
				# row.local = 1
				# fucking sqlAlchemy ...
				# db.engine.execute(Tranche.update().where(Tranche.id == <id>).values(foo="bar"))
				tranche = getTranche(row.trancheID)
				tranche.local = 1

		db.session.commit()

'''
The special tranche tables were created manually like this :

create table  BiogenicTranches as
select trancheName, count(*) as numDrugs,
substring(trancheName, 1, 1) as weight,
substring(trancheName, 2, 1) as logP,
substring(trancheName, 3, 1) as reactivity,
substring(trancheName, 4, 1) as purchasibility,
substring(trancheName, 5, 1) as pH,
substring(trancheName, 6, 1) as charge
from zincLigands join zincToSubset using(zincID) join zincSubsets using(subset) where subsetName='biogenic' group by trancheName
;

'''

WEEDS = 2
DOWNLOAD_PATH = os.path.join(os.getcwd(), 'specialDownload')


def fetchImportantTranches():
	'''
	Download tranches that have lots of FDA/World/Whatever molecules in them
	'''
	from app.core import create_app
	app = create_app(debug=debug)
	with app.app_context():

		def handleQuery(query):
			rows = db.engine.execute(query)
			for row in rows:
				if row.numDrugs < WEEDS:
					print 'Down in the weeds .... exiting here'
					break

				TrancheReader(0, row.urlPath, localCache=DOWNLOAD_PATH)

		query = text('select * from FDATranches join tranches USING(trancheName) order by numDrugs desc;')
		handleQuery(query)
		query = text('select * from WorldTranches join tranches USING(trancheName) order by numDrugs desc;')
		handleQuery(query)
		query = text('select * from InManTranches join tranches USING(trancheName) order by numDrugs desc;')
		handleQuery(query)

def assembleSpecialTranche(subset='fda'):
	from app.core import create_app
	app = create_app(debug=debug)
	with app.app_context():
		query = text('select zincID from zincToSubset join zincSubsets using(subset)where subsetName=:subset;')
		rows = db.engine.execute(query, subset=subset)
		zincIDs = set([r.zincID for r in rows])
		print 'Number of zincIDs to find : ', len(zincIDs)

		# now parse the tranches sequentially
		query = text('''
			select trancheName, urlPath, count(*) as numDrugs
			from zincLigands join zincToSubset using(zincID) join zincSubsets using(subset)
			JOIN tranches using(trancheName)
			where subsetName=:subset
			group by trancheName
			order by numDrugs desc
		;''')
		rows = db.engine.execute(query, subset=subset)
		tranches = []

		outTranche = gzip.open('%s_special.pdbqt.gz' % subset, 'w')

		hitNum = 0

		for row in rows:
			tranches.append(row.urlPath)
			if row.numDrugs<WEEDS: break

			TR = TrancheReader(0, row.urlPath, localCache=DOWNLOAD_PATH)
			modelNum = 1
			while True:
				try: zincID, model = TR.getModel(modelNum)
				except StopIteration: break
				zincID = int(zincID.replace('ZINC',''))
				modelNum+=1
				if zincID in zincIDs:
					print 'Found ', zincID
					hitNum += 1
					outTranche.write('MODEL        %s\n' % str(hitNum))
					outTranche.write(model)
					#outTranche.write('ENDMDL\n')       # not needed, its in model

		outTranche.close()

		print 'Found %s out of %s ligands' % (hitNum, len(zincIDs))


if __name__ == "__main__":
	if args.load:
		load3DTranches()

	if args.special:
		loadSpecialTranches()

	if args.scan:
		findLocalTranches()

	if args.fetch: fetchImportantTranches()

	if args.build: assembleSpecialTranche(subset=args.build)

	if not args.load or args.scan:
		print 'need a command'
	#	args.us