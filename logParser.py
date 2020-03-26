#!/usr/bin/python2.7
import argparse
import glob
import gzip
import os
import shutil

from app.initializers.settings import RESULTS_HOSTING
from app.models import db
from app.models.jobs import Job, getJob

'''

For parsing uploaded logfiles

'''


#set up the flask app

parser = argparse.ArgumentParser()
#parser.add_argument('directory', required=True)
parser.add_argument('-production', action='store_true')
args = parser.parse_args()

debug = True
if args.production: debug = False

from quarantineAtHome.docking.parsers import LogParser

'''
'''

import magic
def validateLogFile(fileName):
	gzMagic = magic.from_buffer(open(fileName).read(2048))
	print gzMagic
	if gzMagic.startswith('gzip compressed data, was "dock.dlg"'):
		fileMagic = magic.from_buffer(gzip.open(fileName).read(2048))
		print fileMagic
		if fileMagic == 'ASCII text': return True

	return False



# scan files after the fact since I waited forever to implement this
# Im going to keep this decoupled from the controller for now, requiring periodic runs from the commandline

def scanDir(db):

	from app.initializers.settings import RESULTS_STORAGE

	for filePath in glob.glob(os.path.join(RESULTS_STORAGE, '*.dlg.gz')):
		path, fileName = os.path.split(filePath)
		good = validateLogFile(filePath)
		jobID = int(fileName.replace('.dlg.gz',''))
		if not good: continue

		#results = parseLogfile(fileName)
		p = LogParser(filePath)
		#outFile = os.path.join(RESULTS_STORAGE, '%d.traj.pdbqt' % jobID)
		#outPath = os.path.join(RESULTS_HOSTING, '%d' % jobID)
		#if not os.path.exists(outPath): os.makedirs(outPath)
		#outFile = os.path.join(outPath, 'trajectory')
		#outFile = os.path.join(RESULTS_HOSTING, '%d.traj.pdbqt' % jobID)
		outFile = os.path.join(RESULTS_HOSTING, '%d.traj.pdbqt' % jobID)
		p.saveTrajectory(outFile)

		# move logfile to hosting area so researchers can download it
		shutil.move(filePath, RESULTS_HOSTING)

		# nah
		#r = Result()
		#r.id = jobID

		if db:
			job = getJob(jobID)
			job.uploaded = True

	if db: db.session.update()


def scanAndInsert():
	from app.core import create_app

	app = create_app(debug=debug)

	with app.app_context():
		#db.create_all()
		# your code here
		scanDir(db)






def printSchema(model):
	# Neat trick to print the create table syntax that would be sent to the server
	from sqlalchemy.schema import CreateTable
	#model = Results
	print(CreateTable(model.__table__))


if __name__ == "__main__":
	#printSchema(Result)
	printSchema(Job)
	scanAndInsert()



