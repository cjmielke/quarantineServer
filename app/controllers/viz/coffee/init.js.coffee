root.mobilecheck = ->
	check = false
	((a) ->
		if /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a) or /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))
			check = true
		return
	) navigator.userAgent or navigator.vendor or window.opera
	check



root.addTracking = (dc) ->

	# GA Goal tracking
	dc.usageCounter = 0
	dc.chartRegistry.list().forEach (chart) ->
		chart.on 'filtered', ->
			# your event listener code goes here.
			dc.usageCounter++
			if dc.usageCounter == 100
				# send event
				console.log 'threshold reached!'
				gtag('event', 'conversion', {'send_to': 'AW-791338680/fPabCPP0v5IBELi9q_kC'});

				#gtag 'event', 'conversion',
				#	'send_to': 'AW-791338680/fPabCPP0v5IBELi9q_kC'
				#	'event_callback': ->
				#		console.log 'callback!'
			console.log 'filter events: ', dc.usageCounter
			return

		return






root.stateCodes =
	1:"Alabama"
	2:"Alaska"
	4:"Arizona"
	5:"Arkansas"
	6:"California"
	8:"Colorado"
	9:"Connecticut"
	10:"Delaware"
	11:"District of Columbia"
	12:"Florida"
	13:"Georgia"
	15:"Hawaii"
	16:"Idaho"
	17:"Illinois"
	18:"Indiana"
	19:"Iowa"
	20:"Kansas"
	21:"Kentucky"
	22:"Louisiana"
	23:"Maine"
	24:"Maryland"
	25:"Massachusetts"
	26:"Michigan"
	27:"Minnesota"
	28:"Mississippi"
	29:"Missouri"
	30:"Montana"
	31:"Nebraska"
	32:"Nevada"
	33:"New Hampshire"
	34:"New Jersey"
	35:"New Mexico"
	36:"New York"
	37:"North Carolina"
	38:"North Dakota"
	39:"Ohio"
	40:"Oklahoma"
	41:"Oregon"
	42:"Pennsylvania"
	44:"Rhode Island"
	45:"South Carolina"
	46:"South Dakota"
	47:"Tennessee"
	48:"Texas"
	49:"Utah"
	50:"Vermont"
	51:"Virginia"
	53:"Washington"
	54:"West Virginia"
	55:"Wisconsin"
	56:"Wyoming"


# replace state codes with integers to enhance performance
#FIXME - THIS IS BULLSHIT
root.stateIDs =
	"AL": 1
	"AK": 2
	"AZ": 3
	"AR": 4
	"CA": 5
	"CO": 6
	"CT": 7
	"DE": 8
	"DC": 9
	"FL": 10
	"GA": 11
	"HI": 12
	"ID": 13
	"IL": 14
	"IN": 15
	"IA": 16
	"KS": 17
	"KY": 18
	"LA": 19
	"ME": 20
	"MT": 21
	"NE": 22
	"NV": 23
	"NH": 24
	"NJ": 25
	"NM": 26
	"NY": 27
	"NC": 28
	"ND": 29
	"OH": 30
	"OK": 31
	"OR": 32
	"MD": 33
	"MA": 34
	"MI": 35
	"MN": 36
	"MS": 37
	"MO": 38
	"PA": 39
	"RI": 40
	"SC": 41
	"SD": 42
	"TN": 43
	"TX": 44
	"UT": 45
	"VT": 46
	"VA": 47
	"WA": 48
	"WV": 49
	"WI": 50
	"WY": 51










root.stateNames =
	"Alabama":"AL"
	"Alaska":"AK"
	"Arizona":"AZ"
	"Arkansas":"AR"
	"California":"CA"
	"Colorado":"CO"
	"Connecticut":"CT"
	"Delaware":"DE"
	"District of Columbia":"DC"
	"Florida":"FL"
	"Georgia":"GA"
	"Hawaii":"HI"
	"Idaho":"ID"
	"Illinois":"IL"
	"Indiana":"IN"
	"Iowa":"IA"
	"Kansas":"KS"
	"Kentucky":"KY"
	"Louisiana":"LA"
	"Maine":"ME"
	"Montana":"MT"
	"Nebraska":"NE"
	"Nevada":"NV"
	"New Hampshire":"NH"
	"New Jersey":"NJ"
	"New Mexico":"NM"
	"New York":"NY"
	"North Carolina":"NC"
	"North Dakota":"ND"
	"Ohio":"OH"
	"Oklahoma":"OK"
	"Oregon":"OR"
	"Maryland":"MD"
	"Massachusetts":"MA"
	"Michigan":"MI"
	"Minnesota":"MN"
	"Mississippi":"MS"
	"Missouri":"MO"
	"Pennsylvania":"PA"
	"Rhode Island":"RI"
	"South Carolina":"SC"
	"South Dakota":"SD"
	"Tennessee":"TN"
	"Texas":"TX"
	"Utah":"UT"
	"Vermont":"VT"
	"Virginia":"VA"
	"Washington":"WA"
	"West Virginia":"WV"
	"Wisconsin":"WI"
	"Wyoming":"WY"






