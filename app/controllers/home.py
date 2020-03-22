from flask import Blueprint, render_template
from sqlalchemy import text

from app.controllers import add_blueprint
from app.models import db

bp = Blueprint('home', __name__, url_prefix='/')


# FIXME - Make a homepage later .... with a table of best results
@bp.route('/')
def index():

	query = text('''SELECT * FROM jobs
		order by bestDG
		LIMIT 50;'''
	)

	rows = db.engine.execute(query)
	#friendDevices = [{'api':r[0], 'url':r[1], 'name':r[2], 'fbid':r[3]} for r in rows]
	#response = {'friendDevices': friendDevices}
	#return jsonify(**response)
	print 'columns :', rows.keys()

	results = []
	for r in rows:
		user = r.user or ''
		zinc = 'ZINC'+str(r.zincID).rjust(12, '0')

		results.append((
			r.jobID,
			user,
			#zinc,
			"<a target='BLANK' href='http://zinc.docking.org/substances/%s/'>%s</a>" % (zinc, zinc),
			r.receptor,
			r.bestDG
		))



	#result = db.engine.execute(sql, user=user)
	#steps = [{'date': r.date.isoformat(), 'steps':r.steps} for r in result]

	return render_template('home.html.jade', results=results)


'''

def getBestFaces(userID, N=10):
	engine = sqlAlchemyCon()
	sql = text('SELECT * FROM faces WHERE user=:user ORDER BY faceScore DESC LIMIT :limit')

	res = engine.execute(sql, user=userID, limit=N)

	lis = []
	for index, row in enumerate(res):
		#print row
		# FIXME - In the future we need to handle other non-facebook image sources
		imgFile = os.path.join(FACEBOOK_PROFILE_IMAGES, row.imgfile)
		lis.append((row.face, imgFile))

	return lis

'''




add_blueprint(bp)
