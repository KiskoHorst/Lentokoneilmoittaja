import planespotters
import flightaware
import jetphotos
import requests
import json
import time

seenPlanes = []
print("Luetaan aircrafts.json")
aircrafts = json.loads(open('aircrafts.json', 'r').read())
print("Luetaan config.json")
config = json.loads(open('config.json', 'r').read())
print("Luetaan newTypes.json")
types = json.loads(open('newTypes.json', 'r').read())

print("Lentokoneiden etsiminen aloitettiin.")
while True:
	currentlyVisible = []
	try:
		req = requests.get(config["aircrafts_json_url"])
		content = json.loads(req.content.decode())
		for plane in content["aircraft"]:
			if "hex" in plane:
				currentlyVisible.append(plane["hex"])
			if (("lat" in plane and "lon" in plane and "gs" in plane and "flight" in plane) or ("rssi" in plane and plane["rssi"] > -15 and plane["messages"] > 200)) and "alt_baro" in plane and "hex" in plane and plane["hex"] not in seenPlanes:
				#print(plane)
				seenPlanes.append(plane["hex"])
				aircraft = {}
				if (plane["hex"].upper() in aircrafts):
					aircraft = aircrafts[plane["hex"].upper()]
					print(aircraft)
				if ("r" in aircraft):
					ps = planespotters.getPlaneInfo(plane["hex"].upper(), aircraft["r"], config["planespotters_session_token"])
					if (ps["photographer"] == None):
						ps = jetphotos.getPlaneInfo(aircraft["r"])
				else:
					ps = planespotters.getPlaneInfo(plane["hex"].upper(), None, config["planespotters_session_token"])
				try:
					fa = flightaware.getFlightData(plane["flight"])
				except:
					fa = None
				route = flightaware.getFlightRoute(fa)
				#ps = {}
				text = "Oho, lentokone!"
				#text = "Testit kännissä!"
				if (ps["photographer"] != None):
					if (ps["photoLink"] != None):
						text += " <a href=\""+ps["photoLink"]+"\">Kuva © "+ps["photographer"]+"</a>"
					else:
						text += " Kuva © "+ps["photographer"]
				text += "\n"
				if (flightaware.getAirline(fa) != None):
					text += "<code>  Yhtiö</code> | "+flightaware.getAirline(fa)+"\n"
				elif ("airline" in ps and ps["airline"] != None):
					text += "<code>  Yhtiö</code> | "+ps["airline"]+"\n"
				else:
					if (ps["photoLink"] != None and not "airline" in ps):
						ps_airline = planespotters.getAirlineFromPhotoLink(ps["photoLink"])
						if (ps_airline != None):
							text += "<code>  Yhtiö</code> | "+ps_airline+"\n"
				if ("flight" in plane):
					text += "<code>  Lento</code> | "+str(plane["flight"])+"\n"
				if (len(route) > 0):
					routetext = route[0]+"\n"
					for airport in route[1:]:
						routetext += "<code>    -> </code> | "+airport+"\n"
					text += "<code> Reitti</code> | "+routetext
				if ("r" in aircraft):
					if (aircraft["d"] == ""):
						if (aircraft["t"] in types and len(types[aircraft["t"]]) > 0):
							text += "<code> Tyyppi</code> | "+types[aircraft["t"]][0]+"\n"
						else:
							text += "<code> Tyyppi</code> | "+aircraft["t"]+"\n"
					else:
						text += "<code> Tyyppi</code> | "+aircraft["d"]+"\n"
					text += "<code> Tunnus</code> | "+aircraft["r"]+"\n"
				#if ("photoUrl" in ps):
				#	text += "Kuva:       "+ps["photoUrl"]+"\n"
				if ("gs" in plane):
					text += "<code> Nopeus</code> | "+str(plane["gs"])+" kt\n"
				text += "<code>Korkeus</code> | "+str(plane["alt_baro"])+" ft\n"
				text += "<code>   ICAO</code> | "+plane["hex"].upper()
				print(text)
				
				
				if (ps["photoUrl"] != None):
					requests.get("https://api.telegram.org/bot"+config["telegram_bot_token"]+"/sendPhoto?parse_mode=HTML&photo="+ps["photoUrl"]+"&caption="+text+"&chat_id="+config["telegram_chat_id"])
				else:
					requests.get("https://api.telegram.org/bot"+config["telegram_bot_token"]+"/sendMessage?parse_mode=HTML&text="+text+"&chat_id="+config["telegram_chat_id"])
			#print(plane)
	except:
		print("error")
	for seenPlane in seenPlanes:
		if seenPlane not in currentlyVisible:
			seenPlanes.remove(seenPlane)
			print(seenPlane+" no longer visible")
	time.sleep(2)
