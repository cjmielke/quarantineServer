

loadPoseTrajectory = (jobID) ->
	stage = document.stage

	# Code for example: interactive/interpolate
	#mol='/static/receptors/mpro-1/poses.pdbqt'
	#mol='/static/52.traj.pdbqt'
	mol='/static/results/'+jobID+'.traj.pdbqt'
	stage.loadFile(mol, asTrajectory: true).then (o) ->
		traj = o.addTrajectory().trajectory
		player = new (NGL.TrajectoryPlayer)(traj,
			step: 1						# how many frames to skip when playing
			timeout: 100				# how many milliseconds to wait between playing frames
			interpolateStep: 5			#
			start: 0					# first frame to play
			end: traj.numframes
			#interpolateType: 'linear'	# linear or spline
			interpolateType: 'spline'
			mode: 'loop'				# either "loop" or "once"
			direction: 'bounce')		# either "forward", "backward" or "bounce"
		player.play()
		o.addRepresentation 'ball+stick'
		o.addRepresentation 'licorice'
		#o.addRepresentation 'spacefill', opacity: 0.6
		#o.autoView()
		return




loadDockingResults = (receptor, jobID) ->
	stage = document.stage

	# Code for example: interactive/annotation
	mol='/static/receptors/'+receptor+'/receptor.pdbqt'
	console.log 'Loading receptor: ', mol
	stage.loadFile(mol).then (o) ->
		o.addRepresentation 'cartoon', color: 'chain'
		#o.addRepresentation 'spacefill', color: 'resname', opacity: 0.5
		o.addRepresentation 'surface', color: 'resname', opacity: 0.9
		#o.addRepresentation 'cartoon'

		###
		chainData =
			'A':
				text: 'alpha subunit'
				color: 'firebrick'
			'B':
				text: 'beta subunit'
				color: 'orange'
			'G':
				text: 'gamma subunit'
				color: 'khaki'
			'R':
				text: 'beta 2 adrenergic receptor'
				color: 'skyblue'
			'N':
				text: 'nanobody'
				color: 'royalblue'

		ap = o.structure.getAtomProxy()

		o.structure.eachChain ((cp) ->
			ap.index = cp.atomOffset + Math.floor(cp.atomCount / 2)
			elm = document.createElement('div')
			elm.innerText = chainData[cp.chainname].text
			elm.style.color = 'black'
			elm.style.backgroundColor = chainData[cp.chainname].color
			elm.style.padding = '8px'
			o.addAnnotation ap.positionToVector3(), elm
			return
		), new (NGL.Selection)('polymer')
		###

		#loadPose()
		loadPoseTrajectory(jobID)

		#return
		#o.autoView()
		pa = o.structure.getPrincipalAxes()
		q = pa.getRotationQuaternion()
		q.multiply o.quaternion.clone().inverse()
		#stage.animationControls.rotate q, 180.0
		#stage.animationControls.move o.getCenter(), 0
		console.log 'Orientation matrix: ', stage.viewerControls.getOrientation()
		document.stage = stage

		#orientation = '{"elements":[26.696642055885402,2.65634782391174,22.085583284800375,0,15.179133339778623,-27.395888441624123,-15.053208084089519,0,16.261091123889955,21.212000910931,-22.207381861213268,0,-7.13700008392334,1.7085000872612,-26.385000228881836,1]}'
		#orientation = '{"elements":[23.101994512069314, 4.683107682230051, 25.532454150878166, 0, 23.578908764996665, -18.081098751762873, -18.018012906376736, 0, 10.856922820904488, 29.303280314984292, -15.198186053368184, 0, -7.13700008392334, 1.7085000872612, -26.385000228881836, 1]}'
		#orientation = receptorOrientations[receptor]
		#orientation = JSON.parse orientation
		root.setReceptorOrientation receptor, stage
		#console.log 'Setting orientation to :', orientation
		#stage.viewerControls.orient orientation.elements


#loadReceptor('mpro-1')


showReceptor = (status) ->
	stage = document.stageReceptor

	receptor = status.receptor
	mol='/static/receptors/'+receptor+'/receptor.pdbqt'
	console.log 'Loading receptor: ', mol
	stage.loadFile(mol).then (o) ->
		o.addRepresentation 'cartoon', color: 'chain'
		#o.addRepresentation 'spacefill', color: 'resname', opacity: 0.5
		o.addRepresentation 'surface', color: 'resname', opacity: 0.9
		#o.addRepresentation 'cartoon'

		#return
		o.autoView()
		stage.setRock true
		root.setReceptorOrientation receptor, stage



showLigand = (status) ->
	stage = document.stageLigand
	console.log 'updates'
	status.zincID = status.ligand
	$('#ligandlink').html('<a href="http://zinc.docking.org/substances/'+status.zincID+'/" target="BLANK">'+status.zincID+'</a>')

	stage.removeAllComponents()

	mol='ligand.pdbqt'
	stage.loadFile(mol, asTrajectory: true).then (o) ->
		traj = o.addTrajectory().trajectory
		o.addRepresentation 'ball+stick'
		o.addRepresentation 'licorice'
		#o.addRepresentation 'spacefill', opacity: 0.6
		o.autoView()
		stage.spinAnimation.axis.set Math.random(),Math.random(),Math.random()
		stage.setSpin true
		return




document.jobs = []
document.ligand = null
document.receptor = null

document.ligands = []
document.ligandStages = []



document.handleUpdate = (status) ->

	# ligand has changed .... outer loop!
	if status.ligand != document.ligand
		document.ligand = status.ligand
		console.log 'Starting new ligand!'
		showLigand(status)

	# next receptor
	if status.receptor != document.receptor
		document.receptor = status.receptor
		console.log 'Receptor has changed!'
		showReceptor(status)



initSettingsPanel = ->

	# prepopulate current values
	$.get('settings.json', (response) ->
		$('#username').val response.username
		return
	'json')

	# register click handler
	$('#settings').submit (event) ->
		event.preventDefault()
		data = {username: $('#username').val()}
		#$.post('config', JSON.stringify(data), (response) ->
		#	console.log 'post result', response
		#	return
		#, 'json')
		# FFS how many times have I had to re-solve this?
		$.ajax
			type: 'POST'
			contentType: "application/json; charset=utf-8"
			url: 'config'
			data: JSON.stringify(data)
			dataType: 'json'
			success: (resp) ->
				console.log resp
				return


start = () ->

	initSettingsPanel()

	addResizeHandler = (stage) ->
		window.addEventListener 'resize', ((event) ->
			#stage.handleResize()
			return
		), false


	if $('.viewport').length
		document.stageLigand = new (NGL.Stage)('ligand', { backgroundColor: "white" })
		addResizeHandler document.stageLigand

		document.stageReceptor = new (NGL.Stage)('receptor')
		addResizeHandler document.stageReceptor

		$('.ligDisplay').each (index) ->
			console.log index
			element = $(this)[0]
			console.log element
			stageDiv = $(this).children('.ligandStage')[0]
			console.log 'stagediv', stageDiv

			link = $(this).children('p')[0]

			stage = new (NGL.Stage)(stageDiv)

			document.ligandStages.push [stage, link]



	taskPoll = (taskID) ->
		$.get('update.json', (response) ->
			#console.log response
			document.handleUpdate response
			return
		'json').fail(->
			console.log 'Couldnt poll for jobs :('
			return
		).always(->
			#setTimeout(taskPoll, 5000)
			return
		)
		return


	taskPoll()




#$(document).ready ->
#document.addEventListener 'DOMContentLoaded', ->
$(document).ready ->
	if Raven?
		Raven.context ->
			start()
			return
	else
		start()





#loadDockingResults = (receptor, jobID) ->
#	loadReceptor(receptor).then (o) ->
#		loadPoseResults(jobID)


