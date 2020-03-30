from os.path import join
from flask_assets import Environment, Bundle
from settings import STATIC_FOLDER

'''
This is mostly holdover from a much larger project (www.infino.me)
assets are stripped but the basic mechanism remains for later
'''



# consolidated css bundle
css_bundle = Bundle(
	'css/style.css',
	#'css/dc.css',

	filters='cssmin', output='css/main.min.css')

coffeeScripts = [
	'coffee/init.js.coffee',
	'coffee/ngl.js.coffee',
]

clientCoffeeScripts = [
	'coffee/init.js.coffee',
	'coffee/client.js.coffee',
]


def register_coffeeScript(path):
	coffeeScripts.append(path)


# this was a sensible idea but I can't figure out
# how to save bundle output to a blueprint-specific location

externalBundles = []
def registerBundle(bundle, name):
	externalBundles.append((bundle, name))




lib_js_bundle = Bundle(
	#'js/d3/d3.v2.min.js',

	#filters='yui_js', output='js/lib.min.js')
	filters = None, output = 'js/lib.min.js')



def init_assets(app):

	coffee_bundle = Bundle(
		*coffeeScripts,
		filters='coffeescript', output='js/coffee.js')

	js_bundle = Bundle(
		#lib_js_bundle,
		coffee_bundle,
		#filters='yui_js',
		output='js/main.min.js')



	clientCoffee = Bundle(
		*clientCoffeeScripts,
		filters='coffeescript', output='js/clientcoffee.js')

	# FIXME - still don't understand why these JS bundles arent compiling ....
	clientJs = Bundle(
		#lib_js_bundle,
		clientCoffee,
		#filters='yui_js',
		output='js/client.min.js')


	#app.config['ASSETS_DEBUG'] = settings.DEBUG
	app.config['ASSETS_DEBUG'] = False
	flaskAssets = Environment(app)

	print 'assets dir is: ', flaskAssets.directory
	print 'root path: ', app.root_path

	flaskAssets.append_path(app.root_path+'/app')
	flaskAssets.append_path(app.static_folder)

	flaskAssets.config['PYSCSS_STATIC_ROOT'] = join(STATIC_FOLDER, 'scss')
	flaskAssets.config['PYSCSS_STATIC_URL'] = join(STATIC_FOLDER, 'css/main.css')
	flaskAssets.config['PYSCSS_DEBUG'] = app.debug

	flaskAssets.register('css', css_bundle)


	flaskAssets.register('coffee', coffee_bundle)
	flaskAssets.register('js', js_bundle)

	flaskAssets.register('clientcoffee', clientCoffee)
	flaskAssets.register('clientjs', clientJs)

	# webassets.manifest = 'cache' if not app.debug else False
	# webassets.cache = not app.debug
	#flaskAssets.cache = False
	flaskAssets.debug = app.debug

	#flaskAssets.debug = False

	for bundle, name in externalBundles:
		flaskAssets.register(name, bundle)


