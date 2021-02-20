from random import shuffle

from flask import Blueprint, render_template, request
from ipaddress import ip_address
from sqlalchemy import text
from app.core import cache
from app.controllers import add_blueprint, jobsTable
from app.initializers.settings import ALL_RECEPTORS, DOCKING_ALGOS
from app.models import db
from app.util import safer

bp = Blueprint('users', __name__, url_prefix='/users')





@bp.route('/')
@cache.cached()
def index():

	# FIXME - this is eventually going to get slow - and will need to be replaced with a cronjob
	query = text('''
		select user, username, count(*) as jobs, group_concat(distinct algo) as algorithms,
		AVG(time) as timeAvg,
		MIN(bestDG) as bestDG
		from users join jobs using(user)
		group by user
	;'''
	)

	rows = db.engine.execute(query)
	print 'columns :', rows.keys()

	cols = [
		'username', 'Completed jobs', 'Code versions', 'Average time per job (seconds)', 'Best Binding Energy'
	]

	results = []
	for r in rows:
		print r
		user = r.username or ''
		user = safer(user)

		userLink = "<a href='/users/%s/'>%s</a>" % (r.user, r.username)

		if r.algorithms:
			algos = ' | '.join([DOCKING_ALGOS[k] for k in r.algorithms.split(',')])
			#algos = r.algorithms
		else: algos=''

		results.append((
			userLink, r.jobs, algos, r.timeAvg, r.bestDG
			#zinc,
			#"<a target='BLANK' href='http://zinc.docking.org/substances/%s/'>%s</a>" % (zinc, zinc),
			#r.bestDG,
			#userLink
		))


	shuffle(results)



	#result = db.engine.execute(sql, user=user)
	#steps = [{'date': r.date.isoformat(), 'steps':r.steps} for r in result]

	return render_template('users.html.jade', results=results, cols=cols)




@bp.route('/<int:userID>/')
@cache.cached(timeout=60*5)
def showUser(userID):

	query = text('''
		select * from jobs
		JOIN users USING(user)
		WHERE user=:user
		ORDER BY bestDG
		LIMIT 300
	;'''
	)

	rows = db.engine.execute(query, user=int(userID))

	results = jobsTable(rows)

	return render_template('user.html.jade', results=results)




add_blueprint(bp)
