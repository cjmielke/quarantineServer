#!/usr/bin/python2.7
import argparse

from app.core import app, create_app

#set up the flask app

parser = argparse.ArgumentParser()
parser.add_argument('-production', action='store_true')


def main():

	args = parser.parse_args()

	debug = True
	if args.production: debug=False

	create_app(debug)
	print 'Debug state: ', app.debug

	host='127.0.0.1'   # host of 0.0.0.0 makes debug server visible over network! Use sparingly

	if debug: host='0.0.0.0'
	app.run(host=host, debug=app.debug, port=1313, threaded=True)

if __name__ == "__main__":
	main()


