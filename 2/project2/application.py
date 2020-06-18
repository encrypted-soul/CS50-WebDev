import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

usernames = []
chatrooms = []
chats = []

@app.route("/")
def index():
    if "username" in session:
        return render_template("chat.html", name=session["username"])
    return render_template("index.html")

@app.route("/enterStatus", methods=["POST"])
def enterStatus():
    name = request.form.get("name")

    if name in usernames:
        return "Please chose another name this name has already been taken."
    else:
        session["username"] = name 
        usernames.append(name)
        return redirect(url_for("chat", name=name))


@app.route("/<name>")
def chat(name):
    return render_template("chat.html", name=name)

