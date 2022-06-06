import requests
import re
import json



def getPlaneInfo(hex, reg, sessiontoken):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
		"Cookie": "ps_sessid="+sessiontoken
	}
	if (reg != None):
		req = requests.get("https://api.planespotters.net/pub/photos/hex/"+hex+"?reg="+reg, headers=headers)
	else:
		req = requests.get("https://api.planespotters.net/pub/photos/hex/"+hex, headers=headers)
	content = json.loads(req.content.decode())
	data = {}
	try:
		data["photographer"] = content["photos"][0]["photographer"]
	except:
		data["photographer"] = None
	
	try:
		data["photoUrl"] = content["photos"][0]["thumbnail_large"]["src"]
	except:
		data["photoUrl"] = None

	try:
		data["photoLink"] = content["photos"][0]["link"]
	except:
		data["photoLink"] = None
	return data

def getAirlineFromPhotoLink(link):
	try:
		req = requests.get(link, headers=headers)
		content = req.content.decode()
		return re.findall("Search for Airline:[^\"]*\">(.*)<\/a>", content)[0].strip()
	except:
		return None