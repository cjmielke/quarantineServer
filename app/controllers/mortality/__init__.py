from flask import Blueprint, render_template

from app.controllers import add_blueprint
from app.initializers.assets import register_coffeeScript

bp = Blueprint('mortality', __name__, url_prefix='/mortality', template_folder='./templates', static_folder='./static')


register_coffeeScript('controllers/mortality/coffee/init.js.coffee')
register_coffeeScript('controllers/mortality/coffee/deathStats.js.coffee')
register_coffeeScript('controllers/mortality/coffee/whoMortality.js.coffee')



@bp.route('/world')
def worldMap(): return render_template('who.html.jade')

@bp.route('/usmap')
def usMap(): return render_template('usmap.html.jade')

@bp.route('/usmap-mobile')
def usMapMobile(): return render_template('usmapMobile.html.jade')






add_blueprint(bp)

