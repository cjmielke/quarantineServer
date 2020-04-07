#!/usr/bin/python2.7
import argparse

from werkzeug.serving import WSGIRequestHandler

from app.core import app, create_app

#set up the flask app
from raven.contrib.flask import Sentry

parser = argparse.ArgumentParser()
parser.add_argument('-debug', action='store_true')



class MyRequestHandler(WSGIRequestHandler):
	# Suppress logging of poll requests every dang second ...
	def log_request(self, code='-', size='-'):
		if 'GET /client/update.json' in self.raw_requestline: return
		super(MyRequestHandler, self).log_request(code, size)



def main():

	args = parser.parse_args()

	debug = False
	if args.debug: debug=True

	create_app(debug)
	print 'Debug state: ', app.debug

	if not debug:
		from app.initializers.secrets import SENTRY_DSN
		sentry = Sentry(app, dsn=SENTRY_DSN)

	host='127.0.0.1'   # host of 0.0.0.0 makes debug server visible over network! Use sparingly

	if debug: host='0.0.0.0'

	if debug:
		app.run(host=host, debug=app.debug, port=1313, threaded=True, request_handler=MyRequestHandler)
	else:
		app.run(host=host, debug=app.debug, port=1313, threaded=True)

if __name__ == "__main__":
	main()


