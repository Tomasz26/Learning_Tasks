import random
from faker import Faker
fake = Faker()
from datetime import datetime

current_date = datetime.now()

# Sformatuj datę w formacie DD.MM.RRRR
formatted_date = current_date.strftime("%d.%m.%Y")

class Movie:
    def __init__(self, title, year, genre, views):
        self.title = title
        self.year = year
        self.genre = genre

        #variables
        self._views = views
    
    def play(self):
        self._views += 1

    def __str__(self):
        return f"{self.title} ({self.year})"

class Series(Movie):
    def __init__(self, title, year, genre, episode, season, views):
        super().__init__(title, year, genre, views)
        self.episode = episode
        self.season = season

    def __str__(self):
        return f"{self.title} S{self.season:02}E{self.episode:02}"

film_library = []
movie_list = []
series_list = []
popular_today = {}

def get_movies(film_library):
    #funkcja sortująca alfabetycznie filmy z kolekcji
    for film in film_library:
        if film.genre == "Movie":
            movie_list.append(film)
    movies_by_name = sorted(movie_list, key=lambda movie: movie.title)
    return movies_by_name

def get_series(film_library):
    #funkcja sortująca alfabetycznie odcinki seriali z kolekcji
    for film in film_library:
        if film.genre == "Series":
            series_list.append(film)
    series_by_name = sorted(series_list, key=lambda movie: movie.title)
    return series_by_name

def get_series_count(film_library, which_series):
    #funkcja licząca ile jest odcinków danego serialu w kolekcji
    count = 0
    for film in film_library:
        if film.title == which_series:
            count += 1
    print(f"There is {count} episodes of {which_series} in library")

def add_series (title, year, genre, season, views, how_many_episodes):
    #funkcja dodająca całe sezony
    for i in range(how_many_episodes):
        film_library.append(Series(title, year, genre, i+1, season, views))

def search(film_list, searched_one):
    #funkcja wyszukująca czy jest w kolekcji dany tytuł
    searched_list = []
    for film in film_list:
        if film.title == searched_one:
            searched_list.append(film)
    if searched_list:
        print("I found the following titles: ")
        for searched in searched_list:
            print(searched)
    else:
        print(f"Unfortunately, I don't have the title {searched_one} in the library")

def generate_views(film_library):
    #funkcja generująca losowe wyświetlenia
    chosen_one = random.choice(film_library)
    add_views = random.randint(1, 100)
    popular_today[chosen_one] = add_views
    chosen_one._views += add_views

def generate_views_10_times():
    #funkcja wyułująca generate_views 10 razy
    for i in range(10):
        generate_views(film_library)

def top_titles_today(popular_today):
    #funkcja wyświetlająca popularne tytuły dzisiaj na podstawie wygenerowanych wyświetleń
    i = 0
    top = sorted(popular_today.items(), key=lambda item: item[1], reverse=True)
    print (f"TOP 3 popular today {formatted_date}:")
    for film, views in top:
        print(film.title)
        i += 1
        if i == 3:
            break

def top_titles(film_library, content_type):
    #funkcja wyświetlająca najczęściej oglądane tytuły wszech czasów w kolekcji
    i = 0
    top = sorted(film_library, key=lambda movie: movie._views, reverse=True)
    print (f"TOP 3 popular {content_type} of all times:")
    for film in top:
        if film.genre == content_type:
            print(film)
            i += 1
        if i == 3:
            break

film_library.append(Movie("Pulp fiction", 1994, "Movie", 2287301))
film_library.append(Movie("Gladiator", 2000, "Movie", 781618))
film_library.append(Movie("One Flew Over the Cuckoo's Nest", 1975, "Movie", 416835))
film_library.append(Movie("Star Wars: Episode III – Revenge of the Sith", 2005, "Movie", 865688))

add_series("Game of thrones", 2011, "Series", 1, 9300000, 10)
add_series("Dr House", 2004, "Series", 1, 5000000, 22)

print("Movie library:")

generate_views_10_times()
#for film in film_library:
#   print(film._views)

#get_series_count(film_library, "Game of thrones")
series_sorted = get_series(film_library)
movies_sroted = get_movies(film_library)

#for film in movies_sorted:
#    print(film)

#for film in series_sorted:
#    print(film)

#search(film_library, "Dune")
top_titles_today(popular_today)
top_titles(film_library, "Movie")