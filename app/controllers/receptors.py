import os
from random import shuffle

import markdown
from flask import Blueprint, render_template, request
from ipaddress import ip_address
from sqlalchemy import text

from app.controllers import add_blueprint
from app.controllers.home import jobsTable
from app.initializers.settings import ALL_RECEPTORS, DOCKING_ALGOS, QUARANTINE_FILES
from app.models import db
from app.util import safer

bp = Blueprint('receptors', __name__, url_prefix='/receptors')


# TODO - finish later
@bp.route('/')
def index():
	return render_template('receptors.html.jade', receptors=ALL_RECEPTORS)



@bp.route('/<receptorName>/')
def showReceptor(receptorName):

	if receptorName not in ALL_RECEPTORS: return 'No receptor with this definition', 404


	receptorDir = os.path.join(QUARANTINE_FILES, 'receptors', receptorName)
	md = open( os.path.join(receptorDir, 'README.md') ).read()

	MD = markdown.Markdown()
	converted = MD.convert(md)

	# super hacky way to rewrite relative links back to github pages  ....
	ghPages = 'https://cjmielke.github.io/quarantine-files/receptors/%s/' % receptorName
	converted = converted.replace('src="img', 'src="%simg'%ghPages)

	md=None         # don't let flask-markdown handle this

	# get top jobs for this receptor

	query = text('''
		select * from jobs
		JOIN users USING(user)
		WHERE receptor=:receptor
		ORDER BY bestDG
		LIMIT 300
	;'''
	)

	rows = db.engine.execute(query, receptor=receptorName)

	results = jobsTable(rows)

	return render_template('receptor.html.jade', receptorName=receptorName, md=md, mymd=converted, results=results)




add_blueprint(bp)
