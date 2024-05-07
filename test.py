import requests
APIkey = "50c2996de269e50e205547980513a419"


APIrequest = f"http://ws.audioscrobbler.com/2.0/?method=album.search&album=believe&api_key={APIkey}&format=json"

file = requests.get(APIrequest)
print(type(file.json()))