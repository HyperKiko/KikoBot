from flask import Flask, redirect, url_for, render_template, request, session, flash
from threading import Thread
import os
import json

with open("config.json", "r") as file:
    configjson = json.load(file)

app = Flask('')
app.secret_key = configjson["web"]["encryption_key"]


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        session.permanent = True
        password = request.form["password"]
        if password == configjson["web"]["password"]:
            session["password"] = password
            flash("Sucessfully logged in.", "success")
            return redirect(url_for("config"))
        else:
            flash("Wrong password!", "danger")
            return redirect(url_for("home"))
    else:
        if "password" in session and session["password"] == configjson["web"]["password"]:
            flash("You are already logged in!", "info")
            return redirect(url_for("config"))
        else:
            return render_template("home.html", config=config, title=os.getenv("REPL_SLUG"))


@app.route("/config")
def config():
    if "password" in session and session["password"] == configjson["web"]["password"]:
        return render_template("config.html")
    else:
        flash("Please log in to continue.", "danger")
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    if "password" in session:
        session.pop("password", None)
        flash("Successfully logged out!", "success")
        return redirect(url_for("home"))
    else:
        flash("Cannot log out because you are not logged in.", "danger")
        return redirect(url_for("home"))


def web():
    if os.getcwd().startswith("/home/runner/") and os.getenv("REPL_SLUG") != None:
        app.run(host='0.0.0.0', port=8080)
    else:
        app.run()


def run():
    t = Thread(target=web)
    t.start()
