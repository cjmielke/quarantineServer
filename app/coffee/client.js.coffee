

loadPoseTrajectory = (stage, mol) ->
	stage.loadFile(mol, asTrajectory: true).then (o) ->
		traj = o.addTrajectory().trajectory
		player = new (NGL.TrajectoryPlayer)(traj,
			step: 1						# how many frames to skip when playing
			timeout: 800				# how many milliseconds to wait between playing frames
			interpolateStep: 10			#
			start: 0					# first frame to play
			end: Math.min(traj.frameCount,2)
			#interpolateType: 'linear'	# linear or spline
			interpolateType: 'spline'
			mode: 'loop'				# either "loop" or "once"
			direction: 'bounce')		# either "forward", "backward" or "bounce"
		console.log 'trajframes', Math.min(traj.frameCount,2)
		player.play()
		o.addRepresentation 'ball+stick', color: 'partialCharge'
		#o.addRepresentation 'licorice'
		#o.addRepresentation 'spacefill', opacity: 0.6
		#o.autoView()
		return




loadDockingResults = (receptor, trajectory) ->
	stage = document.stageReceptor
	stage.removeAllComponents()
	# Code for example: interactive/annotation
	mol='/static/receptors/'+receptor+'/receptor.pdbqt'
	stage.loadFile(mol).then (o) ->
		#o.addRepresentation 'cartoon', color: 'sstruc'
		o.addRepresentation 'cartoon', color: 'residueindex'
		#o.addRepresentation 'cartoon', defaultRepresentation: true
		#o.addRepresentation 'spacefill', color: 'resname', opacity: 0.5
		#o.addRepresentation 'surface', color: 'resname', opacity: 0.9
		#o.addRepresentation 'surface', color: 'chain', opacity: 0.4
		#o.addRepresentation 'cartoon'

		#loadPose()
		loadPoseTrajectory(stage, trajectory)
		root.setReceptorOrientation receptor, stage

#loadReceptor('mpro-1')


showReceptor = (status) ->
	stage = document.stageReceptor
	stage.removeAllComponents()

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
		#stage.setRock true
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




#document.jobs = []

document.ligand = null
document.receptor = null
document.lastJob = null

document.ligands = []
document.ligandStages = []

document.lostConnectionCount = 0


setReceptorName = (rec) ->
	link = "<a href='https://cjmielke.github.io/quarantine-files/receptors/#{rec}/' target='BLANK'>#{rec}</a>"
	$('#receptorName').html link

updateResults = (status) ->
	results = status.lastResults
	$('#pan2').html 'Previous Result'

	setReceptorName results.receptor
	Jid = status.lastJob
	$('#jobID').html "<a href='https://quarantine.infino.me/view/"+Jid+"/' target='BLANK'>"+Jid+"</a>"
	$('#bestDG').html results.bestDG+' kcal/mol'


document.handleUpdate = (status) ->

	# ligand has changed .... outer loop!
	if status.ligand != document.ligand
		document.ligand = status.ligand
		console.log 'Starting new ligand!'
		showLigand(status)


	if status.console
		$('#console').html status.console.join('\n')

	if status.lastResults
		res=status.lastResults
		#setReceptorName res.receptor
		updateResults status
		if status.lastJob != document.lastJob
			document.lastJob = status.lastJob
			loadDockingResults(res.receptor, 'lastTrajectory.pdbqt')
	# next receptor
	else
		if status.receptor != document.receptor
			document.receptor = status.receptor
			setReceptorName(status.receptor)
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


lostConnection = () ->
	#alert 'Lost connection to main program. Note, you need to keep the console window open'
	$('#modal img').attr('src','https://quarantine.infino.me/static/qah-console.png')
	$('.modal').modal('show');




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

		document.stageReceptor = new (NGL.Stage)('receptor', { backgroundColor: "white" })
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
			console.log 'Couldnt poll for jobs :(', document.lostConnectionCount
			document.lostConnectionCount += 1
			if document.lostConnectionCount == 5
				lostConnection()
			return
		).always(->
			setTimeout(taskPoll, 3000)
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


