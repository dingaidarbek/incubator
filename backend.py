from flask import Flask, redirect, url_for, render_template, request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":

        login = request.form["login"]
        password = request.form["password"]
        userAccount = {'login': hash(login.strip()), 'password':hash(password.strip())}

        with open("users.json") as users:  
            usersJson = json.load(users)

        usersJson.append(userAccount)

        with open("users.json", 'w') as json_file:
            json.dump(usersJson, json_file, indent=4, separators=(',',': '))

        return redirect(url_for("user", usr="dimash"))
    
    else:
        return render_template("registration.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/search")
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)