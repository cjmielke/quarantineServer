from flask import Blueprint, render_template, request
from ipaddress import ip_address
from sqlalchemy import text

from app.controllers import add_blueprint, jobsTable
from app.models import db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/crash')
def crash():
	return 1/0

@bp.route('/ip')
def myIP():
	ip = ip_address(unicode(request.remote_addr))
	print ip
	return str(ip)



# FIXME - Make a homepage later .... with a table of best results
@bp.route('/')
def index():

	query = text('''
		SELECT * FROM jobs
		LEFT JOIN users USING(user)
		order by bestDG
		LIMIT 50
	;''')

	rows = db.engine.execute(query)
	#friendDevices = [{'api':r[0], 'url':r[1], 'name':r[2], 'fbid':r[3]} for r in rows]
	#response = {'friendDevices': friendDevices}
	#return jsonify(**response)
	print 'columns :', rows.keys()

	results = jobsTable(rows)


	#result = db.engine.execute(sql, user=user)
	#steps = [{'date': r.date.isoformat(), 'steps':r.steps} for r in result]

	return render_template('home.html.jade', results=results)






add_blueprint(bp)
