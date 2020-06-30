# Setup to load data from rawgit
#NGL.DatasourceRegistry.add 'data', new (NGL.StaticDatasource)('//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/')
# Create NGL Stage object

# Call this function in the browser console to get the orientation string of the NGL viewer
document.printOrientation = () ->
	console.log document.stage.viewerControls.getOrientation().elements



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
		#player.play()
		document.posePlayer = player
		o.addRepresentation 'ball+stick'#, color: 'partialCharge'
		o.addRepresentation 'licorice'
		#o.addRepresentation 'spacefill', opacity: 0.8
		#o.autoView()
		return





#loadReceptor('mpro-1')


loadChainA = (receptor) ->
	stage = document.stage
	#stage.removeAllComponents()
	# Code for example: interactive/annotation
	mol='/static/receptors/'+receptor+'/chainA.pdb'
	stage.loadFile(mol).then (o) ->
		#o.addRepresentation 'cartoon', color: 'sstruc'
		o.addRepresentation 'cartoon', color: 'residueindex', opacity: 0.5, sele: ":A and 25-60"
		#o.addRepresentation 'spacefill', color: 'residueindex', opacity: 0.5
		#o.addRepresentation 'surface', color: 'resname', opacity: 0.5, sele: ":A and 30-46"
		o.addRepresentation "licorice", { sele: ":A and (38 353)" }

		chainData =
			'A':
				text: 'Human ACE2 Receptor'
				color: 'firebrick'

		ap = o.structure.getAtomProxy()

		fun = (cp) ->
			if cp.index==7
				console.log cp
				ap.index = cp.atomOffset + Math.floor(cp.atomCount / 2)
				elm = document.createElement('div')
				elm.innerText = chainData[cp.chainname].text
				elm.style.color = 'black'
				elm.style.backgroundColor = chainData[cp.chainname].color
				elm.style.padding = '8px'
				o.addAnnotation ap.positionToVector3(), elm
			return
		o.structure.eachChain (fun), new (NGL.Selection)('polymer')




loadDockingResults = (receptor, trajectory) ->
	stage = document.stage
	stage.removeAllComponents()
	# Code for example: interactive/annotation
	mol='/static/receptors/'+receptor+'/receptor.pdbqt'
	stage.loadFile(mol).then (o) ->
		#o.addRepresentation 'cartoon', color: 'sstruc'
		o.addRepresentation 'cartoon', color: 'residueindex'
		#o.addRepresentation 'cartoon', defaultRepresentation: true
		#o.addRepresentation 'spacefill', color: 'resname', opacity: 0.5
		o.addRepresentation 'surface', color: 'resname'#, opacity: 0.5
		#o.addRepresentation 'surface', color: 'chain', opacity: 0.4
		#o.addRepresentation 'cartoon'

		if receptor.includes('spike') then loadChainA(receptor)

		#loadPose()
		loadPoseTrajectory(stage, trajectory)
		root.setReceptorOrientation receptor, stage



#$(document).ready ->
document.addEventListener 'DOMContentLoaded', ->

	if $('#viewport').length


		document.stage = new (NGL.Stage)('viewport', { backgroundColor: "white" })
		# Handle window resizing
		window.addEventListener 'resize', ((event) ->
			#stage.handleResize()
			return
		), false

		poses = '/static/results/'+document.jobID+'.traj.pdbqt.gz'

		loadDockingResults(document.receptor, poses)


#loadDockingResults = (receptor, jobID) ->
#	loadReceptor(receptor).then (o) ->
#		loadPoseResults(jobID)


