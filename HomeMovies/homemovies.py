from app import app, db
from app.models import Movie, Actor, Borrowing, movies_actors

@app.shell_context_processor
def make_shell_context():
   return {
       "db": db,
       "Movie": Movie,
       "Actor": Actor,
       "Borrowing": Borrowing,
       "movies_actors": movies_actors
   }