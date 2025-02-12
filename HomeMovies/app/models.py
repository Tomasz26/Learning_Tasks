# app/models.py
from datetime import datetime
from app import db


movies_actors = db.Table(
    "movies_actors",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.id"), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    
    actors = db.relationship("Actor", secondary=movies_actors, back_populates="movies")

    borrowings = db.relationship("Borrowing", backref="movie", lazy="dynamic")

    def __str__(self):
        return f"<Movie {self.title}>"

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    
    movies = db.relationship("Movie", secondary=movies_actors, back_populates="actors")

    def __str__(self):
        return f"<Actor {self.name}>"

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowed = db.Column(db.Boolean, default=True)
    date_borrowed = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_returned = db.Column(db.DateTime, index=True, nullable=True) 
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))

    def __str__(self):
        date = self.date_returned if self.date_returned else self.date_borrowed
        status = "Returned" if self.date_returned else "Borrowed"
        return f"<{status} {self.movie.title} on {date}>"