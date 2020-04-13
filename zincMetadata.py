#!/usr/bin/python2.7
import argparse
import glob
import gzip
import os
import shelve
from collections import Counter


# for example, user provides a path to zincT on commandline
# zincT/AA/ADHN/AAADHN.txt


# gonna just cram into a python shelve database for now
import tqdm as tqdm

# nah - this wasn't wise .....
#DB = shelve.open('ZincMetadata.shelve')
from sqlalchemy import text

from app.core import create_app
from app.models import db, zinc
from app.models.zinc import getSubset, getLigand, LigandSubset

subsets = {}



AllFeatures = Counter()

#class ZincRecord():
#	features = set()



#def getTranches():
#	s = text('SELECT * FROM tranches WHERE ')




def processSpecialFile(name):
	'''
	0:smiles
	1:zinc_id
	2:substance.inchikey
	3:features
	4:tranche_name
	'''

	for line in name:
		line = line.rstrip()
		cols = line.split('\t')

		smiles = cols[0]
		zincID = cols[1]
		assert zincID.startswith('ZINC')
		zincID = int(zincID.replace('ZINC',''))

		# print zincID, smiles
		features = cols[3]

		assert len(cols) == 5

		features = features.split(' ')
		for name in features:
			AllFeatures[name] += 1

			if name not in subsets:
				setID = getSubset(name)
				subsets[setID]=name



def process3Dfile(f):

	header = f.readline()
	#print 'Header : ', header
	'''
	0:smiles
	1:zinc_id
	2:prot_id
	3:files.db2
	4:substance.inchikey
	5:net_charge
	6:ph_mod_fk
	7:substance.mwt
	8:substance.logp
	9:purchasable
	10:reactive
	11:features
	12:tranche_name
	'''
	# smiles	zinc_id	prot_id	files.db2	substance.inchikey	net_charge	ph_mod_fk	substance.mwt	substance.logp	purchasable	reactive	features	tranche_name

	for line in f:
		line = line.rstrip()
		cols = line.split('\t')

		assert len(cols) == 13

		smiles = cols[0]
		zincID = cols[1]
		assert zincID.startswith('ZINC')
		zincID = int(zincID.replace('ZINC',''))


		# print zincID, smiles
		features = cols[11].split(' ')


		if len(features):           # only storing zincID's present in special subsets for now

			ligand = getLigand(zincID)
			ligand.smiles = cols[0]
			ligand.protID = cols[2]
			ligand.InChI = cols[4]
			ligand.charge = cols[5]
			ligand.ph = cols[6]
			ligand.weight = cols[7]
			ligand.logP = cols[8]
			ligand.trancheName = cols[12]
			db.session.add (ligand)

			#ins = text('INSERT IGNORE INTO zincToSubset () VALUES ()')
			#db.cursor.execut(ins)
			for f in features:
				s = LigandSubset(zinc=zincID, subset=subsets[f])
				db.session.add(s)

		db.session.commit()     # after every file




def scan(args):

	pbar = tqdm.tqdm(total=39466)       # determined on commandline after rsyncing ....


	debug=True
	if args.production: debug=False


	App = create_app(debug=debug)


	with App.app_context():
		db.create_all()


		for txtFile in glob.iglob(args.dir+'/*/*/??????.txt.gz'):
			path, filename = os.path.split(txtFile)
			#print txtFile
			#print path, filename

			tranche = filename.replace('.txt.gz', '')

			try:
				with gzip.open(txtFile, 'r') as f:
					if '/special/' in txtFile:
						process3Dfile(f)
					elif '/3D' in txtFile:
						process3Dfile(f)
			except Exception as e:
				print e

			pbar.update()




def stats():
	count=0
	for key in DB:
		zr = DB[key]  # type: ZincRecord
		for f in zr.features: AllFeatures[f] += 1
		#print key, zr.features
		count+=1

	print AllFeatures.most_common(50)
	print count

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	# parser.add_argument('directory', required=True)
	parser.add_argument('-production', action='store_true')
	parser.add_argument('-dir', help='Directory structure with zinc metadata text files')
	parser.add_argument('-stats', action='store_true')
	args = parser.parse_args()

	if args.dir:
		if not os.path.exists(args.dir):
			raise ValueError('No directory found at ', args.dir)
		scan(args)

	if args.stats:
		stats()

