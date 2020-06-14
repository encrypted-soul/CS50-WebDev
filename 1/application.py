import os
from passlib.hash import sha256_crypt

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/signUpComplete", methods=["POST"])
def signUpComplete():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    password = sha256_crypt.encrypt(password)

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        db.execute("INSERT INTO users (username, password, name) VALUES (:username, :password, :name)", 
        {"name": name, "username": username, "password": password})
        db.commit()
        session["username"] = username
        return redirect(url_for("user", username=username))
    else:
        return "The entered username has already been taken please enter some other username"

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/loginStatus", methods=["POST"])
def loginStatus():
    username = request.form.get("username")
    password = request.form.get("password")

    check_password = db.execute("SELECT password from users WHERE username = :username", {"username": username}).fetchone()[0]
    if sha256_crypt.verify(password, check_password):
        session["username"] = username
        return redirect(url_for("user", username=username))
    else:
        return "don't mess with me"

@app.route("/<username>")
def user(username):
    if "username" in session:
        user = session["username"]
        name = db.execute("SELECT name from users WHERE username = :username", {"username": user}).fetchone()[0]
        return render_template("usr.html", name=name)
    else:
        return redirect(url_for("login"))

@app.route("/user/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/search", methods=["POST"])
def search():
    book = ("%" + request.form.get("searchstr") + "%")

    results = db.execute("""SELECT title FROM books WHERE id LIKE (:book) OR UPPER(title) LIKE UPPER((:book)) OR UPPER(author) LIKE UPPER((:book))""", {"book" : book})
    return render_template("usr.html", titles=results)

@app.route("/book/<title>", methods=["GET"])
def book(title):
    results = db.execute("SELECT * from books WHERE title = :title", {"title": title}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "zyJVAQ7oh3HV7AfCSWOasw", "isbns": results[0]})
    data = res.json()
    apidata = (data["books"][0]["work_ratings_count"], data["books"][0]["average_rating"])
    return render_template("books.html", results=results, apidata=apidata)

@app.route("/review/<index>", methods=["POST"])
def postreview(index):
    review = request.form.get('review')
    ratings = 3
    if "username" in session:
        username = session['username']
        name = db.execute("SELECT name from users WHERE username = :username", {"username": username}).fetchone()[0]
        db.execute("INSERT INTO reviews (book_id, username, name, review, ratings) VALUES (:id, :username, :name, :review, :ratings)", 
        {"id": index, "username": username, "name": name, "review": review, "ratings": ratings})
        db.commit()
    results = db.execute("SELECT * from books WHERE id = :id", {"id": index}).fetchone()
    reviews = db.execute("SELECT review from reviews WHERE book_id = :id", {"id": index}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "zyJVAQ7oh3HV7AfCSWOasw", "isbns": results[0]})
    data = res.json()
    apidata = (data["books"][0]["work_ratings_count"], data["books"][0]["average_rating"])
    return render_template("books.html", reviews=reviews, results=results, apidata=apidata)