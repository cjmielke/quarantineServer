from flask import render_template

from app.initializers.settings import ALL_RECEPTORS
from app.util import safer


def error_page(message):
	return render_template('shared/error.html.jade', message=message)

_blueprints = []


def loadControllers(app):
	from app.controllers import home
	from app.controllers.api import v1
	from app.controllers import ngl
	from app.controllers import client, users, receptors, job

	for blueprint in _blueprints:
		app.register_blueprint(blueprint)

	return

def add_blueprint(blueprint):
	_blueprints.append(blueprint)


def zincPad(zincID):
	return 'ZINC' + str(zincID).rjust(12, '0')

def zincLink():
	"<a target='BLANK' href='http://zinc.docking.org/substances/%s/'>%s</a>" % (zincName, zincName)

def receptorLink(receptor):
	ol = "<a target='BLANK' href='https://github.com/cjmielke/quarantineAtHome/tree/master/receptors/%s'>%s</a>" % (receptor, receptor)
	return "<a target='BLANK' href='/receptors/%s'>%s</a>" % (receptor, receptor)

def resultLink(jobID):
	return "<a target='BLANK' href='/job/%s/'>Results</a>" % (jobID)

def userLink(row):
	if row.username:
		userName = safer(row.username)
		return "<a href='/users/%s/'>%s</a>" % (row.user, userName)
	else: return ''


class ZincDisp():
	def __init__(self, zincID):
		self.zincID = zincID

	@property
	def pad(self): return 'ZINC' + str(self.zincID).rjust(12, '0')

	@property
	def name(self): return 'ZINC' + str(self.zincID)

	@property
	def link(self):
		return "<a target='BLANK' href='http://zinc.docking.org/substances/%s/'>%s</a>" % (self.pad, self.name)



class RowFormatter:
	def __init__(self, resultProxy, columns=None):

		if columns and type(columns)==str: columns=columns.split(' ')

		self.columns = columns or resultProxy.keys()

		self.results = []
		for row in resultProxy:

			if row.receptor not in ALL_RECEPTORS: continue  # defense against injection

			rows = []
			for col in self.columns:
				val = row[col]
				if col=='receptor': val = receptorLink(val)
				if col=='results' and row.uploaded: val = resultLink(row.jobID)
				if col=='zinc': val = ZincDisp(row.zincID).link
				if col=='user': val = userLink(row)
				rows.append(val)

			self.results.append(row)





# TODO - build in exclusion lists for specific columns
def jobsTable(rows):

	results = []
	for r in rows:

		if r.username:
			userName = safer(r.username)
			userDisp = "<a href='/users/%s/'>%s</a>" % (r.user, userName)
		else: userDisp=''


		zinc = 'ZINC'+str(r.zincID).rjust(12, '0')

		if r.receptor not in ALL_RECEPTORS: continue			# defense against injection

		if r.uploaded: resultsLink = "<a target='BLANK' href='/job/%s/'>Results</a>" % (r.jobID)
		else: resultsLink = ''

		results.append((
			r.jobID,
			userDisp,
			#zinc,
			"<a target='BLANK' href='http://zinc.docking.org/substances/%s/'>%s</a>" % (zinc, zinc),
			"<a target='BLANK' href='https://github.com/cjmielke/quarantineAtHome/tree/master/receptors/%s'>%s</a>" % (r.receptor, r.receptor),
			r.bestDG,
			resultsLink
		))

	return results