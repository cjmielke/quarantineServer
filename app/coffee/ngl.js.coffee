# Setup to load data from rawgit
#NGL.DatasourceRegistry.add 'data', new (NGL.StaticDatasource)('//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/')
# Create NGL Stage object

# Call this function in the browser console to get the orientation string of the NGL viewer
document.printOrientation = () ->
	console.log document.stage.viewerControls.getOrientation().elements


receptorOrientations =
	'mpro-1': '{"elements":[23.101994512069314, 4.683107682230051, 25.532454150878166, 0, 23.578908764996665, -18.081098751762873, -18.018012906376736, 0, 10.856922820904488, 29.303280314984292, -15.198186053368184, 0, -7.13700008392334, 1.7085000872612, -26.385000228881836, 1]}'
	'spike-1': '{"elements":[-10.248018011734107, 53.494595049708416, -52.82097738332285, 0, -57.02228201005461, -40.27164793961613, -29.722095333674165, 0, -48.99170037493601, 35.682935657340394, 45.64307857361319, 0, -6.055524473477347, 3.0221278137468803, -82.51501341525847, 1]}'



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


loadPose = () ->
	stage = document.stage

	mol='/static/receptors/mpro-1/pose0.pdbqt'
	stage.loadFile(mol).then (o) ->
		rep = 'ball+stick'
		rep = 'spacefill'
		o.addRepresentation rep #, color: ''
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

		o.autoView()
		pa = o.structure.getPrincipalAxes()
		q = pa.getRotationQuaternion()
		q.multiply o.quaternion.clone().inverse()
		stage.animationControls.rotate q, 0
		stage.animationControls.move o.getCenter(), 0
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
		orientation = receptorOrientations[receptor]
		orientation = JSON.parse orientation
		console.log 'Setting orientation to :', orientation
		stage.viewerControls.orient orientation.elements


#loadReceptor('mpro-1')


#$(document).ready ->
document.addEventListener 'DOMContentLoaded', ->

	if $('#viewport').length


		document.stage = new (NGL.Stage)('viewport')
		# Handle window resizing
		window.addEventListener 'resize', ((event) ->
			#stage.handleResize()
			return
		), false


		loadDockingResults(document.receptor, document.jobID)


#loadDockingResults = (receptor, jobID) ->
#	loadReceptor(receptor).then (o) ->
#		loadPoseResults(jobID)


