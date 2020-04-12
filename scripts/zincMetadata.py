#!/usr/bin/python2.7
import argparse
import glob
import os
import shelve
from collections import Counter


# for example, user provides a path to zincT on commandline
# zincT/AA/ADHN/AAADHN.txt


# gonna just cram into a python shelve database for now

DB = shelve.open('ZincMetadata.shelve')


AllFeatures = Counter()

class ZincRecord():
	features = set()


def processFile(f):

	header = f.readline()
	print 'Header : ', header
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

		smiles = cols[0]
		zincID = cols[1]
		assert zincID.startswith('ZINC')

		# print zincID, smiles
		features = cols[11]

		assert len(cols) == 13

		if zincID not in DB:
			DB[zincID] = ZincRecord()

		zr = DB.get(zincID)

		for f in features.split(' '):
			AllFeatures[f] += 1
			zr.features.add(f)


def scan(args):

	for txtFile in glob.iglob(args.dir+'/*/*/??????.txt'):
		print txtFile

		path, filename = os.path.split(txtFile)

		print path, filename

		tranche = filename.replace('.txt', '')

		with open(txtFile, 'r') as f:
			processFile(f)

		print AllFeatures.most_common(50)

		DB.sync()

	DB.close()



def stats():
	for key in DB:
		zr = DB[key]  # type: ZincRecord
		for f in zr.features: AllFeatures[f] += 1
		print key, zr.features

	print AllFeatures.most_common(50)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	# parser.add_argument('directory', required=True)
	parser.add_argument('-dir', help='Directory structure with zinc metadata text files')
	parser.add_argument('-stats', action='store_true')
	args = parser.parse_args()

	if args.dir:
		scan(args)

	if args.stats:
		stats()

