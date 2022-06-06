import requests
import re
import json

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

def getPlaneInfo(reg):
	try:
		req = requests.get("https://www.jetphotos.com/showphotos.php?aircraft=all&airline=all&country-location=all&photographer-group=all&category=all&keywords-type=reg&keywords-contain=0&keywords="+reg+"&photo-year=all&genre=all&search-type=Advanced&sort-order=0")
		content = req.content.decode().split("<div class=\"result\"")[1]
		
		data = {}
		
		try:
			data["photographer"] = re.search("By: <a href=\"\/photographer\/[0-9]*\/photos\" class=\"link\">(.*)<\/a><\/", content)[1]
		except:
			data["photographer"] = None

		try:
			data["airline"] = re.search("Airline: <a href=\"\/airline\/[a-zA-Z0-9 ]*\" class=\"link\">(.*)<\/a><\/", content)[1]
		except:
			data["airline"] = None
		
		try:
			data["photoUrl"] = "https://"+(re.search("<img src=\"\/\/(.*)\" class=\"result__photo\"", content)[1])
		except:
			data["photoUrl"] = None
		
		try:
			data["photoLink"] = "https://jetphotos.com"+(re.search("<a href=\"(.*)\" class=\"result__photoLink\">", content)[1])
		except:
			data["photoLink"] = None
		return data
	except:
		return None