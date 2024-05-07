from flask import Flask, redirect, url_for, render_template, request, session
import json
import requests
from datetime import timedelta

app = Flask(__name__)
APIkey = "50c2996de269e50e205547980513a419"
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

    
@app.route("/", methods=["POST", "GET"])
def home():
    APIrequest = f"http://ws.audioscrobbler.com/2.0/?method=album.gettoptags&artist=radiohead&album=the%20bends&api_key={APIkey}&format=json"
    file = requests.get(APIrequest)
    return render_template("home.html", data = file.json()["toptags"]["tag"])


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
    if request.method == "POST":
        search = request.form.get("searching", False)
        APIrequest = f"http://ws.audioscrobbler.com/2.0/?method=album.search&album={search}&api_key={APIkey}&format=json"
        file = requests.get(APIrequest)
        return render_template("search.html", results = file.json()["results"]["albummatches"]["album"])
    else:
        return render_template("search.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)