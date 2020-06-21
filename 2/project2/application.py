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
chatrooms = ['random', 'general']
chats = []

@app.route("/")
def index():
    if "username" in session:
        return render_template("chat.html", name=session["username"], chatrooms=chatrooms)
    return render_template("index.html")

@app.route("/enterStatus", methods=["POST"])
def enterStatus():
    name = request.form.get("name")

    if name not in usernames:
        usernames.append(name)

    session["username"] = name 
    return redirect(url_for("chat", name=name))


@app.route("/<name>")
def chat(name):
    return render_template("chat.html", name=name, chatrooms=chatrooms)

@app.route("/changeName")
def changeName():
    session.pop("username", None)
    return render_template("index.html")

@app.route("/create_channel_status", methods=["POST", "GET"])
def create_channel_status():
    channel_name = request.form.get("channel_name")
    chatrooms.append(channel_name)
    return render_template("chat.html", name=session["username"], chatrooms=chatrooms)