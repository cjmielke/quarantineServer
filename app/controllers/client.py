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

@bp.route('update.json')
def lastJob():
	lj = {"tranche": 446, "ligand": 1, "user": None, "receptor": "mpro-1", "algo": "AD4", "time": 167.92191004753113, "bestDG": -3.35, "meanDG": -2.283529411764706, "zincID": "ZINC000008384274"}
	lj = {"lastResults": {"tranche": 158, "ligand": 1, "zincID": "ZINC000004018039", "receptor": "mpro-1", "user": None, "time": 112.50104594230652, "bestDG": -7.74, "meanDG": -6.891666666666666, "algo": "AD4"}, "receptor": "spike-1", "ligand": "ZINC000004018039", "lastJob": 101}
	return jsonify(**lj)



# an endpoint for testing the client-side javascript for configuring program settings
clientSettings = dict(username='anonymousB')

@bp.route('settings.json', methods=['GET','POST'])
def settings():
	if request.method == 'GET':
		return jsonify(**clientSettings)

@bp.route('config', methods=['GET','POST'])
def config():
	if request.method == 'GET':
		return jsonify(**clientSettings)
	if request.method == 'POST':
		assert request.is_json
		j = request.get_json()
		#print request.form['username']
		#clientSettings['username'] = request.form['username']
		clientSettings['username'] = j['username']
		response = {'status': 'ok'}
		return jsonify(**response)



ligand = '''
REMARK  Name = ZINC000069639911
REMARK                            x       y       z     vdW  Elec       q    Type
REMARK                         _______ _______ _______ _____ _____    ______ ____
ROOT
ATOM      1  C   LIG    1       -1.294   1.936   0.019  0.00  0.00    -0.360 A 
ATOM      2  C   LIG    1       -2.507   1.244   0.027  0.00  0.00    +0.280 A 
ATOM      3  N   LIG    1       -3.647   1.922   0.036  0.00  0.00    -0.620 NA
ATOM      4  C   LIG    1       -3.683   3.237   0.038  0.00  0.00    +0.340 A 
ATOM      5  N   LIG    1       -2.557   3.997   0.031  0.00  0.00    -0.630 NA
ATOM      6  C   LIG    1       -1.342   3.404   0.027  0.00  0.00    +0.490 A 
ATOM      7  O   LIG    1       -0.320   4.066   0.021  0.00  0.00    -0.580 OA
ENDROOT
BRANCH   4   8
ATOM      8  C   LIG    1       -5.000   3.914   0.049  0.00  0.00    +0.270 A 
ATOM      9  C   LIG    1       -6.182   3.169   0.063  0.00  0.00    -0.030 A 
ATOM     10  C   LIG    1       -7.389   3.852   0.073  0.00  0.00    +0.290 A 
ATOM     11  N   LIG    1       -7.381   5.174   0.069  0.00  0.00    -0.540 NA
ATOM     12  C   LIG    1       -6.247   5.848   0.056  0.00  0.00    +0.460 A 
ATOM     13  N   LIG    1       -5.078   5.244   0.052  0.00  0.00    -0.480 NA
ENDBRANCH   4   8
BRANCH   1  15
ATOM     14  O   LIG    1        0.002  -0.004   0.002  0.00  0.00    -0.730 OA
ATOM     15  C   LIG    1       -0.015   1.220   0.009  0.00  0.00    +0.540 C 
ATOM     16  O   LIG    1        1.037   1.846   0.002  0.00  0.00    -0.690 OA
ENDBRANCH   1  15
TORSDOF 2
ENDMDL
'''

@bp.route('/ligand.pdbqt')
def sendLigand():
	return ligand





add_blueprint(bp)


