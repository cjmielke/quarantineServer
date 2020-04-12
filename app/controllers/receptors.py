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

def renderMarkdownFromGithub(mdFile, baseURL):
	'''Opens markdown file stored in quarantine-files repository, parses it, and replaces image urls'''
	md = open(mdFile).read()

	MD = markdown.Markdown()
	converted = MD.convert(md)

	# super hacky way to rewrite relative links back to github pages  ....
	converted = converted.replace('src="img', 'src="%simg' % baseURL)

	return converted


@bp.route('/')
def index():

	mdFile = os.path.join(QUARANTINE_FILES, 'receptors', 'README.md')
	baseURL = 'https://cjmielke.github.io/quarantine-files/receptors/'
	converted = renderMarkdownFromGithub(mdFile, baseURL)

	return render_template('receptors.html.jade', mymd=converted)



@bp.route('/<receptorName>/')
def showReceptor(receptorName):

	if receptorName not in ALL_RECEPTORS: return 'No receptor with this definition', 404

	receptorDir = os.path.join(QUARANTINE_FILES, 'receptors', receptorName)
	mdFile = os.path.join(receptorDir, 'README.md')

	baseURL = 'https://cjmielke.github.io/quarantine-files/receptors/%s/' % receptorName

	converted = renderMarkdownFromGithub(mdFile, baseURL)

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
