from flask import render_template

def error_page(message):
	return render_template('shared/error.html.jade', message=message)

_blueprints = []


def loadControllers(app):
	from app.controllers import home
	from app.controllers.api import v1

	for blueprint in _blueprints:
		app.register_blueprint(blueprint)

	return

def add_blueprint(blueprint):
	_blueprints.append(blueprint)



