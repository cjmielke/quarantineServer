#!/usr/bin/python2.7
import argparse
import glob
import gzip
import os
import shutil

from app.initializers.settings import RESULTS_HOSTING
from app.models import db, printSchema
from app.models.jobs import Job, getJob

'''

For parsing uploaded logfiles

'''


#set up the flask app

parser = argparse.ArgumentParser()
#parser.add_argument('directory', required=True)
parser.add_argument('-dev', action='store_true')
args = parser.parse_args()

debug = False
if args.dev: debug = True

from quarantineAtHome.docking.parsers import LogParser

'''
'''

import magic
def validateLogFile(fileName):
	gzMagic = magic.from_buffer(open(fileName).read(2048))
	#print gzMagic
	if gzMagic.startswith('gzip compressed data, was'):
		fileMagic = magic.from_buffer(gzip.open(fileName).read(2048))
		#print fileMagic
		terminators_ = ['ASCII text', 'ASCII text, with CRLF line terminators',
		                'ASCII text, with CRLF, CR line terminators']
		if fileMagic in terminators_:
			return True
		else:
			print 'filemagic is not valid : ', fileMagic
			return False
	else:
		print 'GZMAGIC is not valid :', gzMagic
		return False


from app.initializers.settings import RESULTS_STORAGE


# scan files after the fact since I waited forever to implement this
# Im going to keep this decoupled from the controller for now, requiring periodic runs from the commandline

def scanDir(db):
	pass


def scanAndInsert():
	from app.core import create_app

	app = create_app(debug=debug)

	with app.app_context():
		#db.create_all()
		# your code here

		if debug:
			for n in range(10):
				j = Job()
				j.receptor = 'mpro-1'
				db.session.add(j)
				db.session.commit()


		for filePath in glob.glob(os.path.join(RESULTS_STORAGE, '*.dlg.gz')):
			path, fileName = os.path.split(filePath)
			good = validateLogFile(filePath)
			jobID = int(fileName.replace('.dlg.gz',''))
			if not good:
				print filePath, ' is not good'
				continue

			job = getJob(jobID)
			if not job:
				print 'Cannot find job ', jobID
				continue


			#results = parseLogfile(fileName)

			try: p = LogParser(filePath)
			except Exception as e:
				print e
				continue


			#outFile = os.path.join(RESULTS_STORAGE, '%d.traj.pdbqt' % jobID)
			#outPath = os.path.join(RESULTS_HOSTING, '%d' % jobID)
			#if not os.path.exists(outPath): os.makedirs(outPath)
			#outFile = os.path.join(outPath, 'trajectory')
			#outFile = os.path.join(RESULTS_HOSTING, '%d.traj.pdbqt' % jobID)
			outFile = os.path.join(RESULTS_HOSTING, '%d.traj.pdbqt.gz' % jobID)
			p.saveTrajectory(outFile, compress=True)

			# move logfile to hosting area so researchers can download it
			dst = os.path.join(RESULTS_HOSTING, fileName)
			shutil.move(filePath, dst)

			# nah
			#r = Result()
			#r.id = jobID

			job.uploaded = True
			db.session.commit()


if __name__ == "__main__":
	#printSchema(Result)
	printSchema(Job)
	scanAndInsert()



