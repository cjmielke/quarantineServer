if $('#usa-mortality').length
	if mobilecheck() and document.location.pathname == '/mortality/usmap'
		document.location = 'usmap-mobile'
		$('#mobile').show()

	if not mobilecheck() and document.location.pathname == '/mortality/usmap-mobile'
		document.location = 'usmap'






numberFormat = d3.format('.2f')
root.usChart = dc.geoChoroplethChart('#us-chart')
root.timeSeriesPlot = dc.barChart("#timeseries-chart")
#root.timeSeriesPlot = dc.lineChart("#timeseries-chart")

#root.causeChart = dc.rowChart("#cause-chart")
root.chapterChart = dc.rowChart("#icd-chapter")

root.ldbdTested = dc.rowChart("#leaderboard-tested")
root.ldbdConfirmed = dc.rowChart("#leaderboard-confirmed")
root.ldbdDead = dc.rowChart("#leaderboard-dead")

root.genderChart = dc.pieChart('#gender-chart')
root.bubbleChart = dc.bubbleChart('#bubble-chart')


normalize = (chart) ->
	data = (d.value / stateDeathTotals[d.key] for d in chart.data())
	e = d3.extent(data)
	if e[1]==e[0]
		e = [0,2]
	#e[0]=0
	#console.log e
	chart.colorDomain e
	return

#usChart.on 'preRender', (chart) ->
#	normalize chart

#usChart.on 'preRedraw', (chart) ->
#	normalize chart



makeChart = (tsv, minDate, maxDate, total_deceased) ->
	#console.log tsv
	root.tsv = tsv
	#parseTime = d3.time.format('%Y-%m-%d')

	#root.stateDeathTotals = {}
	#for key of stateCodes
	#	stateName = stateNames[stateCodes[key]]
	#	stateDeathTotals[stateName] = 0


	console.log 'Date range:', minDate, maxDate


	d3.json 'static/us-states.json', (statesJson) ->

		dw = $(document).width()

		ndx = crossfilter(tsv)


		root.states = ndx.dimension (d) ->
			#console.log d.stateID
			d.state

		root.stateDeaths = states.group().reduceSum (d) ->
			d.deaths


		$('.viz').show()








		mapWidth = $('#us-chart').width()
		projection = d3.geo.albersUsa().scale(mapWidth).translate([mapWidth/2,250])

		usChart.width(mapWidth).height(500)
		.projection(projection)
		.dimension(states).group(stateDeaths)
		.colors(d3.scale.quantize().range(["#FFEBD6", "#F5CBAE", "#EBA988", "#E08465", "#D65D45", "#CC3527", "#C40A0A"]))
		.valueAccessor (d) ->
			#d.value.population
			#d.value.deaths*100000.0 / d.value.population
			#d.value / stateDeathTotals[d.key]
			val = d.value / total_deceased
			#console.log val
			val*10
		#.title (d) ->
		#	'State: ' + d.key + '\nPercent of Deaths\nin this state :  ' + 100.0*d.value

		.overlayGeoJson statesJson.features, 'state', (d) ->
			d.properties.name






		causeDim = ndx.dimension (d) ->
			d.icd
		causeGroup = causeDim.group().reduceSum (d) ->
			d.deaths

		###
		causeChart.width($('#cause-chart').width()).height(1000)
		.dimension(causeDim).group(causeGroup)
		.rowsCap(30)
		.ordering (d) ->
			-d.value
		.label (d) ->
			#d.key+' | '+ICDSubchapters[d.key]
			ICDSubchapters[ICDCodes[d.key]]
		.elasticX(true).othersGrouper(false).renderLabel(true).transitionDuration(1000).xAxis()
		.tickFormat (v) ->
			''
		###









		dateDim = ndx.dimension (d) ->
			d.date
		deathGroup = dateDim.group().reduceSum (d) ->
			d.deaths

		metricGroup = dateDim.group().reduce(((p, v) ->
			++p.count
			p.new_tested += v.new_tested
			p.new_confirmed += v.new_confirmed
			p.new_deceased += v.new_deceased
			p
		), ((p, v) ->
			--p.count
			p.new_tested -= v.new_tested
			p.new_confirmed -= v.new_confirmed
			p.new_deceased -= v.new_deceased
			p
		), ->
			{
				count: 0
				new_tested: 0
				new_confirmed: 0
				new_deceased: 0

			}
		)



		timeSeriesPlot
		#.renderArea(true)
		.width($('#timeseries-chart').width()+15).height(200)
		.margins({top: 10, right: 0, bottom: 30, left: 70})
		.dimension(dateDim)
		#.group(deathGroup)
		.group(metricGroup, 'New Tested')
		.valueAccessor (d) ->
			d.value.new_tested
		.stack metricGroup, 'New Confirmed', (d) ->
			d.value.new_confirmed
		#.elasticY(true)#.round(dc.round.floor).gap(1).alwaysUseRounding(true)
		#.x(d3.scale.linear().domain([0,13]))
		.x(d3.time.scale().domain([minDate,maxDate])).xUnits(d3.time.weeks)
		.renderHorizontalGridLines(true).centerBar(true).elasticY(true).legend(dc.legend().x(85).y(10))
		#.title (d) ->
		#	d.key + '\n: Time  Asleep: ' + Math.round(d.value.stageS) + '\nTime Restless: ' + Math.round(d.value.stageR)
		#.x(d3.scale.ordinal().domain(['0','1','2','3','4','5','6','7','8','9','a','b','c']))
		#.colors(colorbrewer.RdYlGn[9])
		#.colorAccessor (d) ->
		#	d.key
		#.colorDomain([0,18])
		.elasticY(true)
		#timeSeriesPlot.xAxis().tickFormat (v) ->
		#	deathGroups[v]
		#timeSeriesPlot.xAxis().ticks 15
		timeSeriesPlot.yAxis().ticks 5
		#timeSeriesPlot.yAxis().ticks 0





		genderDim = ndx.dimension (d) ->
			d.gender
		genderGroup = genderDim.group().reduceSum (d) ->
			d.deaths

		# gender
		w = $('#gender-chart').width() - 5
		console.log 'pie width:', w
		genderChart.width(w).height(180).radius(65).innerRadius(30)
		.dimension(genderDim).group(genderGroup)
		.renderLabel(false)
		.legend(dc.legend().x(w/2-10).y(70).itemHeight(10).gap(5))
		.colors d3.scale.ordinal().domain(['M','F','?']).range(['#3E85FD','#F590E5','#DDD'])



		getAvg = (p, count, prop) ->
			if p.value[count] then p.value[prop] / p.value[count] else 0


		stateDim = ndx.dimension (d) ->
			d.state

		# dimension by state
		stateGroup = stateDim.group().reduce(((p, v) ->
			++p.count
			p.new_tested += v.new_tested
			p.new_confirmed += v.new_confirmed
			p.new_deceased += v.new_deceased

			p.positiveRate = p.new_confirmed / p.new_tested
			p
		), ((p, v) ->
			--p.count
			p.new_tested -= v.new_tested
			p.new_confirmed -= v.new_confirmed
			p.new_deceased -= v.new_deceased

			p.positiveRate = p.new_confirmed / p.new_tested

			p
		), ->
			{
				count: 0
				new_confirmed: 0
				new_tested: 0
				new_deceased: 0

				total_tested: 0
				total_confirmed: 0
				total_deceased: 0

				positiveRate: 0
			}
		)

		bubbleWidth = $('#bubble-chart').width()
		bubbleHeight = Math.min(bubbleWidth, 400)
		#alert bubbleWidth

		bubbleChart.width(bubbleWidth).height(bubbleHeight)
		.margins({top: 10, right: 50, bottom: 30, left: 40})
		.transitionDuration(1500).dimension(stateDim).group(stateGroup)

		.xAxisPadding(1000)
		.x(d3.scale.linear().domain([ 0, 100000 ])).elasticX(true)
		.xAxisLabel('Number tested').keyAccessor (p) ->
			#getAvg p, 'count', 'new_confirmed'
			#console.log p
			p.value.total_tested

		.y(d3.scale.linear()).elasticY(true)
		.yAxisPadding(500)
		.yAxisLabel('Number Dead').valueAccessor (p) ->
			avg = getAvg(p, 'count', 'new_tested')
			#if avg < 500
			#	avg = 1500
			# hide users with no calorie counts
			avg

		.colors(colorbrewer.RdYlGn[9]).colorDomain([ 0, 100 ])
		.colorAccessor (p) ->
			getAvg p, 'count', 'new_deceased'

		.r(d3.scale.linear().domain([ 0, 100000 ]))
		.radiusValueAccessor (p) ->
			getAvg p, 'count', 'new_tested'





		.maxBubbleRelativeSize(0.07)
		.renderHorizontalGridLines(true).renderVerticalGridLines(true)\
		.legend(dc.legend().x(0).y(10).itemHeight(13).gap(5)).renderLabel(true)
		.label (p) ->
			'' + p.key
		#	'' + users[p.key].name












		chapterGroup = stateDim.group().reduceSum (d) ->
			d.deaths

		chapterChart.width($('#icd-chapter').width()).height(450)
		.dimension(stateDim).group(chapterGroup)
		.label (d) ->
			d.key+' | '+ d.value
		.ordering (d) ->
			-d.value
		.elasticX(true).rowsCap(17).othersGrouper(false).renderLabel(true).transitionDuration(1000).xAxis()
		.tickFormat (v) ->
			''

		rowsCap = 7
		height = 200
		tickFmt = (v) ->
			v/1000+'k'


		testedGroup = stateDim.group().reduceSum (d) ->
			d.new_tested
		ldbdTested.width($('#leaderboard-tested').width()).height(height)
		.dimension(stateDim).group(testedGroup)
		.ordering (d) ->
			-d.value
		.elasticX(true).rowsCap(rowsCap).othersGrouper(false).renderLabel(true).transitionDuration(1000).xAxis()
		.tickFormat tickFmt




		ldbdConfirmed.width($('#leaderboard-confirmed').width()).height(height)
		.dimension(stateDim).group(stateGroup)
		.valueAccessor (d) ->
			d.value.positiveRate
		.label (d) ->
			d.key+' | '+ parseInt(100*d.value.positiveRate) + '%'
		.ordering (d) ->
			-d.value.positiveRate
		.elasticX(true).rowsCap(rowsCap).othersGrouper(false).renderLabel(true).transitionDuration(1000).xAxis()
		.tickFormat tickFmt

		deadGroup = stateDim.group().reduceSum (d) ->
			d.new_deceased
		ldbdDead.width($('#leaderboard-dead').width()).height(height)
		.dimension(stateDim).group(deadGroup)
		.label (d) ->
			d.key+' | '+ d.value
		.ordering (d) ->
			-d.value.new_deceased
		.elasticX(true).rowsCap(rowsCap).othersGrouper(false).renderLabel(true).transitionDuration(1000).xAxis()
		.tickFormat tickFmt









		dc.renderAll()

		root.addTracking(dc)

		$('#loading').hide()

		return


	return








$(document).ready ->

	return if not $('#usa-mortality').length

	$('#loading').show()


	deathGroups =
		'0': '1'
		'1': '1-4'
		'2': '5-9'
		'3': '10-14'
		'4': '15-19'
		'5': '20-24'
		'6': '25-34'
		'7': '35-44'
		'8': '45-54'
		'9': '55-64'
		'10': '65-74'
		'11': '75-84'
		'12': '85+'
		'x': 'NS'

	stateCodes = root.stateCodes		# old
	stateNames = root.stateNames









	file = 'static/state-epi.tsv'
	#file = 'static/foo.tsv'

	minDate = undefined
	maxDate = undefined
	total_deceased = 0

	tsv = []
	parseTime = d3.time.format('%Y-%m-%d')
	d3.tsv file, (data) ->

		data.forEach (d) ->

			#d.state = stateNames[stateCodes[+d.state]]
			#d.deaths = +d.deaths
			d.deaths = +d.new_deceased
			total_deceased += d.deaths
			#if d.stateID==undefined then return
			#d.age = parseInt(d.age,16)

			#stateDeathTotals[d.state] += d.deaths
			#d.chapter = ICD10(ICDCodes[d.icd])

			dd = parseTime.parse(d.date)
			d.date = dd

			d.new_tested = +d.new_tested
			d.new_confirmed = +d.new_confirmed
			d.new_deceased = +d.new_deceased
			d.new_recovered = +d.new_recovered

			d.total_tested = +d.total_tested
			d.total_confirmed = +d.total_confirmed
			d.total_deceased = +d.total_deceased
			d.total_recovered = +d.total_recovered

			#if d.state==undefined
			#	console.log 'nostate'


			if minDate == undefined
				minDate = dd
				maxDate = dd
			if dd < minDate
				minDate = dd
			if dd > maxDate
				maxDate = dd

			tsv.push d

			return


		console.log minDate, maxDate
		makeChart tsv, minDate, maxDate, total_deceased


	#d3.tsv file, (tsv) ->
	#	makeChart tsv



	return
