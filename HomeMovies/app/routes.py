from flask import request, redirect, url_for, render_template
from app import app, db
from app.models import Movie, Borrowing, Actor
from datetime import datetime

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies")
def movie_list():
    movies = Movie.query.all()
    for movie in movies:
        movie.last_borrowing = movie.borrowings.order_by(Borrowing.date_borrowed.desc()).first()

    return render_template("movie_shelf.html", movies=movies)

@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            new_movie = Movie(title=title)
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for("movie_list"))

    return render_template("add_movie.html")

@app.route("/add_actor", methods=["GET", "POST"])
def add_actor():
    movies = Movie.query.all()

    if request.method == "POST":
        name = request.form.get("name")
        movie_ids = request.form.getlist("movie_ids[]")

        if name and movie_ids:
            new_actor = Actor(name=name)
            db.session.add(new_actor)
            db.session.commit()

            for movie_id in movie_ids:
                movie = Movie.query.get(movie_id)
                if movie:
                    movie.actors.append(new_actor)

            db.session.commit()
            return redirect(url_for("movie_list"))

    return render_template("add_actor.html", movies=movies)

@app.route("/borrow_movie", methods=["GET", "POST"])
def borrow_movie():
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        if movie_id:
            borrowing = Borrowing(movie_id=movie_id, date_borrowed=datetime.utcnow())
            db.session.add(borrowing)
            db.session.commit()
        return redirect(url_for("borrow_movie"))

    movies = Movie.query.all()
    borrowings = Borrowing.query.all()
    return render_template("borrow.html", movies=movies, borrowings=borrowings)

@app.route("/return_movie/<int:borrowing_id>", methods=["POST"])
def return_movie(borrowing_id):
    borrowing = Borrowing.query.get(borrowing_id)
    if borrowing and borrowing.date_returned is None:
        borrowing.date_returned = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("borrow_movie"))