from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

class Reviews(db.Model):
    __tablename__ = "reviews"
    book_id = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    ratings = db.Column(db.Integer, nullable=False)