from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import text

from app.controllers import add_blueprint
from app.initializers.settings import ALL_RECEPTORS
from app.models import db
from app.models.jobs import getJob, Job

bp = Blueprint('client', __name__, url_prefix='/client')


'''
The whole point of this controller is to build the static page assets for the local client

This allows me to develop the client interface using jade/pug templates and coffeescript, and also
easily deploy updates to the client interface
'''


@bp.route('/')
def index():
	return render_template('client/client.html.jade')

@bp.route('/index.html')
def index2():
	return render_template('client/client.html.jade')

@bp.route('lastJob.json')
def lastJob():
	lj = {"tranche": 446, "ligand": 1, "user": None, "receptor": "mpro-1", "algo": "AD4", "time": 167.92191004753113, "bestDG": -3.35, "meanDG": -2.283529411764706, "zincID": "ZINC000008384274"}
	return jsonify(**lj)

# an endpoint for testing the client-side javascript for configuring program settings
clientSettings = dict(username='anonymous')
@bp.route('/config', methods=['GET','POST'])
def config():
	if request.method == 'GET':
		return jsonify(**clientSettings)
	if request.method == 'POST':
		content = request.get_json()
		for key in content.keys():
			clientSettings[key] = content[key]
		#return jsonify(**{'status', 'okay'})
		return jsonify(**clientSettings)



add_blueprint(bp)


