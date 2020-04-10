# import urllib3.contrib.pyopenssl
# urllib3.contrib.pyopenssl.inject_into_urllib3()

from flask import Flask
# from flask_cache import Cache
from pyjade.ext.jinja import PyJadeExtension

from app.initializers import settings
from app.initializers.assets import init_assets
from app.models import db
from app.models.jobs import testModels

# from app.auth import loginManagerSetup

app = Flask('quarantine', static_folder=settings.STATIC_FOLDER,
            template_folder=settings.TEMPLATE_FOLDER)
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800

# Caching
# cache = Cache(config={'CACHE_TYPE': 'simple'})


def register_blueprints(app):
    from app.controllers import loadControllers
    loadControllers(app)


def create_app(debug):
    '''creates app instance, db instance, and apimanager instance'''

    # Extra config stuff
    app.config['DEBUG'] = debug
    # if debug:
    #    app.config['PROPAGATE_EXCEPTIONS'] = False
    #    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

    # Generate DB URI
    if debug:
        db_uri = settings.SQLALCHEMY_SQLITE_URI
    else:                # for production
        from app.initializers import secrets
        db_uri = 'mysql://%s:%s@localhost/%s' % (settings.MYSQL_USER, secrets.MYSQL_PASSWORD, settings.MYSQL_DB)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.secret_key = SECRET_KEY  # move this out of here eventually

    # Templating engines
    # Flask.jinja_options['extensions'].append(SlimishExtension)
    Flask.jinja_options['extensions'].append(PyJadeExtension)

    db.init_app(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # toolbar = DebugToolbarExtension(app)

    # Set up user management
    app.config['CSRF_ENABLED'] = True
    app.config['USER_ENABLE_EMAIL'] = False

    # load blueprints
    register_blueprints(app)

    # Initialize assets
    init_assets(app)

    with app.app_context():
        db.create_all()

        if debug:
            testModels()

    return app
