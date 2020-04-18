from flask import Blueprint, render_template
from sqlalchemy import text

from app.controllers import add_blueprint
from app.initializers.settings import ALL_RECEPTORS
from app.models import db
from app.models.jobs import getJob, Job, User

bp = Blueprint('job', __name__, url_prefix='/job')



@bp.route('/<int:jobID>/')
def showJob(jobID):
	#job = getJob(jobID)
	job = Job.query.get_or_404(jobID)		# better
	user = User.query.get(job.user)


	query = text('''
	SELECT * FROM jobs
	LEFT JOIN users USING(user)
	WHERE jobID=:jobID
	;''')
	res=db.engine.execute(query, jobID=jobID)
	row=res.first()

	hidecols = ['ip', 'uploaded', 'trancheID', 'trancheLigand', 'user', 'jobID']

	table = {}
	keys = res.keys()
	#keys = 'username receptor algo zincID bestDG'.split(' ')
	for k in keys:
		if k in hidecols: continue
		val = row[k] or ''
		table[k] = val

	if row.username:
		table['username'] = '<a href="/users/%d">%s</a>' % (int(row.user), table['username'])

	table['receptor'] = '<a href="/receptors/%s">%s</a>' % (row.receptor, row.receptor)


	return render_template('job.html.jade', id=job.id, job=job, user=user, row=row, table=table)



add_blueprint(bp)


