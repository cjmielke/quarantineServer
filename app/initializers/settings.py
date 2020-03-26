import os
from os.path import join


# I use this to make development easy - better ways to do this
import socket
HOSTNAME = socket.gethostname()


# The root location of the app. Should not need to be changed.
ROOT_DIR=os.path.realpath(join(join(os.path.dirname(__file__), os.path.pardir), os.path.pardir))

# Static content
STATIC_FOLDER = ROOT_DIR + '/app/static'

# Templates
TEMPLATE_FOLDER = ROOT_DIR + '/app/templates'

# Whether or not to cache decoder results. When True, will not re-run the
# decoder on an image unless the image has been modified since the
# last decoding; when False, will re-run the decoder every time.
CACHE_DECODINGS = True



### DATABASE CONFIGURATION ###
#SQL_ADAPTER = 'mysql'
#SQL_ADAPTER = 'sqlite'
#if not DEBUG: SQL_ADAPTER = 'mysql'

# SQLite path
SQLALCHEMY_SQLITE_URI = 'sqlite:///' + 'sqlite.db'

# MySQL configuration
#MYSQL_USER = 'root'
MYSQL_USER = 'quarantine'
#MYSQL_PRODUCTION_DB = 'app'
#MYSQL_DEVELOPMENT_DB = 'app'
MYSQL_DB = 'quarantine'

ALL_RECEPTORS = ['mpro-1', 'spike-1']

LIVE_RECEPTORS = ALL_RECEPTORS				# receptors currently being assigned



LOCAL_ZINC = os.path.join(os.getcwd(), 'ZINCDB')

RESULTS_STORAGE = os.path.join(os.getcwd(), 'DLG')
RESULTS_HOSTING = os.path.join(STATIC_FOLDER, 'results')

DOCKING_ALGOS = ['AD4', 'AD-gpu', 'AD-vina', 'AD-win']