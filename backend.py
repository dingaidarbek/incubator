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
        userAccount = {'login': login, 'password':password}
        with open("users.json", "w") as users:  
            users.write(json.dumps(userAccount,indent=4))

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