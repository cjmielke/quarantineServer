from flask import Blueprint

from app.controllers import add_blueprint

bp = Blueprint('api',__name__,url_prefix='/api')



add_blueprint(bp)


