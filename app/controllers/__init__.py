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