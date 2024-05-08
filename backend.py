from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import requests
from datetime import timedelta
# Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import http.client

os.environ["SPOTIPY_CLIENT_ID"] = '895ebdcb42a240fd906aebb862a08646'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'c415b1d0d68f425191af25f1fa934ea7'


# Authenticate with Spotify using the Client Credentials flow
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__)
APIkey = "50c2996de269e50e205547980513a419"
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("album", albumID = request.form.get("getAlbumID")))
    else:
        # Use the country from the query parameters, if provided
        if 'country' in request.args:
            country = request.args['country']
        else:
            country = 'SE'      
        # Send request to the Spotify API
        new_releases = sp.new_releases(country=country, limit=20, offset=0)
        # Return the list of new releases
        # return jsonify(new_releases)
        APIrequest = "https://api.spotify.com/v1/browse/new-releases"
        with open(".cache", "r") as tokenFile:
            token = json.load(tokenFile)["access_token"]
            conn = http.client.HTTPSConnection("")
            headers = { 'authorization': f"Bearer {token}" }
            # conn.request("GET","https://api.spotify.com/v1/", "me", headers=headers)
            file = requests.get(APIrequest, headers=headers)
            # res = conn.getresponse()
            # data = res.read()
            # dataResult = data.decode("utf-8")
        # finalDict = str_to_dict(dataResult)
        return render_template("home.html", data = file.json()["albums"]["items"]) + str(file.json()["albums"]["items"])


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        repeatPassword = request.form["repeatPassword"]
        if password == repeatPassword:
            # userAccount = {'login': hash(login.strip()), 'password':hash(password.strip())} #with encoding
            userAccount = {'login': login.strip(), 'password':password.strip()} # without encoding
            with open("users.json") as users:  
                usersJson = json.load(users)

            usersJson.append(userAccount)

            with open("users.json", 'w') as json_file:
                json.dump(usersJson, json_file, indent=4, separators=(',',': '))

            return redirect(url_for("user", usr=login))
        else:
            return "password does not match" + render_template("registration.html")
    else:
        return render_template("registration.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        userAccount = {'login': hash(login.strip()), 'password':hash(password.strip())}

        with open("users.json") as users:  
            usersJson = json.load(users)

        for user in usersJson:
            if user["login"] == login:
                if user["password"] == password:
                            return redirect(url_for("user", usr=login))
    else:
        return render_template("login.html")
    
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST" and "searching" in request.form:
        search = request.form.get("searching", False)
        APIrequest = f"https://api.spotify.com/v1/search?q={search}&type=album"
        with open(".cache", "r") as tokenFile:
            token = json.load(tokenFile)["access_token"]
            conn = http.client.HTTPSConnection("")
            headers = { 'authorization': f"Bearer {token}" }
            file = requests.get(APIrequest, headers=headers)
        return render_template("search.html", results = file.json()["albums"]["items"]) + str(file.json()["albums"]["items"])
        # return render_template("search.html", results = file.json()["results"]["albummatches"]["album"])
    elif request.method == "POST" and "getAlbumID" in request.form:
        return redirect(url_for("album", albumID = request.form.get("getAlbumID")))
    else:
        return render_template("search.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/album?albumID=<albumID>', methods=["POST", "GET"])
def album(albumID):
    APIrequest = "https://open.spotify.com/oembed?url=https%3A%2F%2Fopen.spotify.com%2Falbum%2F" + albumID
    with open(".cache", "r") as tokenFile:
        token = json.load(tokenFile)["access_token"]
        conn = http.client.HTTPSConnection("")
        headers = { 'authorization': f"Bearer {token}" }
        file = requests.get(APIrequest, headers=headers)
    return render_template("album.html", data = file.json()["html"]) + str(file.json()["html"])

# @app.route('/authorize')
# def authorize():
#   client_id = app.config['CLIENT_ID']
#   redirect_uri = app.config['REDIRECT_URI']
#   scope = app.config['SCOPE']
#   state_key = createStateKey(15)
#   session['state_key'] = state_key

#   authorize_url = 'https://accounts.spotify.com/en/authorize?'
#   params = {'response_type': 'code', 'client_id': client_id,
#             'redirect_uri': redirect_uri, 'scope': scope, 
#             'state': state_key}
#   query_params = urlencode(params)
#   return redirect(authorize_url + query_params)

    return False
def str_to_dict(string):
    # remove the curly braces from the string
    string = string.strip('{}')
 
    # split the string into key-value pairs
    pairs = string.split(', ')
 
    # use a dictionary comprehension to create
    # the dictionary, converting the values to
    # integers and removing the quotes from the keys
    return {key[1:-2]: int(value) for key, value in (pair.split(': ') for pair in pairs)}

if __name__ == "__main__":
        app.run(debug=True)