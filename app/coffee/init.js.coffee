root = exports ? this


$(document).ready ->
	if Raven?
		Raven.config('https://94e7e20880d44b37a13fb770c8476a3e@bugs.infino.me/8').install()
		root.raven = Raven
	else
		console.log 'Sentry is not loaded'
		root.raven = null


receptorOrientations =
	'mpro-1': '{"elements":[23.101994512069314, 4.683107682230051, 25.532454150878166, 0, 23.578908764996665, -18.081098751762873, -18.018012906376736, 0, 10.856922820904488, 29.303280314984292, -15.198186053368184, 0, -7.13700008392334, 1.7085000872612, -26.385000228881836, 1]}'
	'spike-1': '{"elements":[-10.248018011734107, 53.494595049708416, -52.82097738332285, 0, -57.02228201005461, -40.27164793961613, -29.722095333674165, 0, -48.99170037493601, 35.682935657340394, 45.64307857361319, 0, -6.055524473477347, 3.0221278137468803, -82.51501341525847, 1]}'

setReceptorOrientation = (receptor, stage) ->
	if receptor of receptorOrientations
		j = receptorOrientations[receptor]
		orientation = JSON.parse j
		console.log 'Setting orientation to :', orientation
		stage.viewerControls.orient orientation.elements
	else
		console.log 'receptor not defined in orientations list'



