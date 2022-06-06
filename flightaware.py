import requests
import re
import json

def getFlightData(flightnum):
	attempts = 0
	while attempts < 3:
		try:
			req = requests.get("https://flightaware.com/live/flight/"+flightnum)
			jsonstr = re.findall("<script>var trackpollBootstrap = (.*);<\/script>", req.content.decode())[0]
			data = json.loads(jsonstr)
			return data
		except:
			print("error in flightaware: "+flightnum)
			attempts+=1
	return None

def getFlightRoute(data):
	try:
		flights = data["flights"][next(iter(data["flights"]))]["activityLog"]["flights"]
		flight = flights[0]
		foundFlight = False
		for dataFlight in flights:
			if (dataFlight["flightStatus"] == "airborne"):
				flight = dataFlight
				break
		def airportDataToName(airport):
			return (airport["friendlyName"]+" ("+airport["iata"]+"/"+airport["icao"]+")")
		if flight["destination"]["isValidAirportCode"]:
			return [
				airportDataToName(flight["origin"]),
				airportDataToName(flight["destination"])
			]
		else:
			if len(flights) >= 4 and (flights[1]["destination"]["icao"] == flights[2]["destination"]["icao"] == flights[3]["destination"]["icao"]) and (flight["origin"]["icao"] == flights[1]["origin"]["icao"] == flights[2]["origin"]["icao"] == flights[3]["origin"]["icao"]):
				prev_flight = data["flights"][next(iter(data["flights"]))]["activityLog"]["flights"][1]
				if prev_flight["destination"]["isValidAirportCode"]:
					return [
						airportDataToName(flight["origin"]),
						airportDataToName(prev_flight["destination"])
					]
		return [
			airportDataToName(flight["origin"])
		]
	except:
		return []

def getAirline(data):
	try:
		flight = data["flights"][next(iter(data["flights"]))]
		return flight["airline"]["shortName"]
	except:
		return None