#!/usr/bin/python2.7
import argparse

from app.core import app, create_app

#set up the flask app

parser = argparse.ArgumentParser()
parser.add_argument('-debug', action='store_true')


def main():
	args = parser.parse_args()
	create_app(args.debug)
	print 'Debug state: ', app.debug

	host='127.0.0.1'   # host of 0.0.0.0 makes debug server visible over network! Use sparingly

	if args.debug: host='0.0.0.0'
	app.run(host=host, debug=app.debug, port=5001, threaded=True)

if __name__ == "__main__":
	main()


