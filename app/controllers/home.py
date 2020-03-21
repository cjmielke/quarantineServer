from flask import Blueprint
from sqlalchemy import text

from app.controllers import add_blueprint

bp = Blueprint('home', __name__, url_prefix='/')


q=text('SELECT * FROM quarantine.jobs order by bestDG;')



add_blueprint(bp)
