from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import requests
from datetime import timedelta
# Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import http.client
from datetime import datetime
import sys

os.environ["SPOTIPY_CLIENT_ID"] = '895ebdcb42a240fd906aebb862a08646'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'c415b1d0d68f425191af25f1fa934ea7'


# Authenticate with Spotify using the Client Credentials flow
sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials())

app = Flask(__name__)
APIkey = "50c2996de269e50e205547980513a419"
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

response = sp.new_releases()
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("album", albumID = request.form.get("getAlbumID")))
    else:
        sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials())
        file = sp.new_releases()
        return render_template("home.html", data = file["albums"]["items"])


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        repeatPassword = request.form["repeatPassword"]
        if password == repeatPassword:
            userAccount = {'login': hash(login.strip()), 'password':hash(password.strip())} #with encoding
            with open("users.json") as users:  
                usersJson = json.load(users)

            usersJson.append(userAccount)

            with open("users.json", 'w') as json_file:
                json.dump(usersJson, json_file, indent=4, separators=(',',': '))

            session.permanent = True
            session["user"] = login

            return redirect(url_for("home"))
        else:
            return "password does not match" + render_template("registration.html")
    else:
        return render_template("registration.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        login = request.form["login"]
        password = request.form["password"]
        userAccount = {'login': hash(login.strip()), 'password':hash(password.strip())}

        with open("users.json") as users:  
            usersJson = json.load(users)

        session["user"] = login

        for user in usersJson:
            if user["login"] == login:
                if user["password"] == password:
                            return redirect(url_for("account"))
    else:
        return render_template("login.html")
    
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST" and "searching" in request.form:
        if "searching" == "":
            return render_template("search.html")
        search = request.form.get("searching", False)
        APIrequest = f"https://api.spotify.com/v1/search?q={search}&type=album"
        sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials())
        file = sp.search(search, type= "album")

        return render_template("search.html", results = file["albums"]["items"])
    elif request.method == "POST" and "getAlbumID" in request.form:
        return redirect(url_for("album", albumID = request.form.get("getAlbumID")))
    else:
        return render_template("search.html")

@app.route('/logout')
def logout():
    session["user"] = None
    return redirect(url_for('login'))

@app.route('/album/<albumID>', methods=["POST", "GET"])
def album(albumID):
    APIrequest = "https://open.spotify.com/oembed?url=https%3A%2F%2Fopen.spotify.com%2Falbum%2F" + albumID
    file = requests.get(APIrequest)
    with open("comments.json") as comments:
        commentsJson = json.load(comments)
        commentsSection = []
        if albumID in commentsJson: 
            commentsSection = commentsJson[albumID]
    
    if request.method == "POST" and "comment" in request.form:
        if "user" not in session or session["user"] == None:
            newComment = {"userLogin":"Anonym", "date": str(datetime.now())[:16], "comment":request.form.get("comment", "NOCOMMENT")}
        else:
            newComment = {"userLogin":session["user"], "date": str(datetime.now())[:16], "comment":request.form.get("comment", "NOCOMMENT")}
        
        with open("comments.json") as comments:
            commentsJson = json.load(comments)
        if albumID in commentsJson:
            commentsJson[albumID].append(newComment)
        else:
            commentsJson[albumID] = [newComment]

        with open("comments.json", 'w') as json_file:
            json.dump(commentsJson, json_file, indent=4, separators=(',',': '))
            
    return render_template("album.html", data = file.json(), comments = commentsSection)


def str_to_dict(string):
    string = string.strip('{}')
    pairs = string.split(', ')
    return {key[1:-2]: int(value) for key, value in (pair.split(': ') for pair in pairs)}

@app.route('/account')
def account():
    if "user" not in session or session["user"] == None:
        return redirect(url_for('login'))
    return render_template("account.html", account = session["user"])

if __name__ == "__main__":
        app.run(debug=True)
