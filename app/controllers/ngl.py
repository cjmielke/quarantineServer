from flask import Blueprint, render_template
from sqlalchemy import text

from app.controllers import add_blueprint
from app.initializers.settings import ALL_RECEPTORS
from app.models import db
from app.models.jobs import getJob, Job

bp = Blueprint('ngl', __name__, url_prefix='/view')


@bp.route('/')
def index():

	return render_template('ngl.html.jade')


@bp.route('/<int:jobID>/')
def showPoses(jobID):
	#job = getJob(jobID)
	job = Job.query.get_or_404(jobID)		# better
	return render_template('ngl.html.jade', id=job.id, job=job)



add_blueprint(bp)


