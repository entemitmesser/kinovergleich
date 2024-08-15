#!/Users/moritzruttkowski/Mucino/.venv/bin/python3
from scrapers.mathaeser_scraper import mScraper
from scrapers.cinemaxx_scraper import cmScraper
import sqlite3
import os

mt = mScraper()
cm = cmScraper()
try:
    os.mkdir("data")
except:
    pass
conn = sqlite3.connect("data/movie_data.db")
db = conn.cursor()

#db setup
try:
    db.execute("DROP TABLE movies")
    db.execute("DROP TABLE playtimes")
except:
    pass
db.execute("""CREATE TABLE movies (
        title text,
        location text,
        url text
)""")
db.execute("""CREATE TABLE playtimes (
        title text,
        price text,
        raw_date text,
        date text   
)""")
conn.commit()
conn.close()

def mathaeser():
    movies = []
    for movie in mt.getAllMovies():
        movie_data = {}
        movie_data["title"] = movie
        playtime_price_tuples = list(zip(mt.findDatesForMovies()[movie], mt.findPriceForMovies()[movie]))

        movie_data["playtime_price"] = []
        for tuple in playtime_price_tuples:
            playtime = tuple[0]
            price = tuple[1]
            movie_data["playtime_price"].append(f"{playtime} +++ {price}\n")

        movie_data["location"] = {"name":"Mathäser Filmpalast", "url":"https://www.mathaeser.de/mm/"}
        movies.append(movie_data)

    return(movies)

def cinemaxx():
    movies = []
    movie_table_data, playtime_data = cm.getMovieData()
    for movie in movie_table_data:
        movie_data = {}
        movie_data["title"] = movie
        #movie_data["raw_date"] = cm.getMovieData()[movie]["raw_date"]
        #playtime_price_tuples = list(zip(cm.getMovieData()[movie]["playtime"], cm.getMovieData()[movie]["price"]))
        ##print(playtime_price_tuples)

        #movie_data["playtime_price"] = []

        #for tuple in playtime_price_tuples:
        #    playtime = tuple[0]
        #    price = cm.getMovieData()[movie]["price"].replace(",", ".")
        #    movie_data["playtime_price"].append(f"{playtime} +++ {price}\n")

        movie_data["location"] = {"name":"Cinemaxx", "url":"https://www.cinemaxx.de/kinoprogramm/munchen/"}
        movies.append(movie_data)

    return(movies, playtime_data)

def populate_db():
    cm_movie_data, cm_playtime_data = cinemaxx()
    all_movies = []
    local_c = sqlite3.connect("data/movie_data.db")
    local_db = local_c.cursor()
    #local_db.execute(f"SELECT * FROM movies WHERE title=?", (f'{movie}',))
    #mathaeser
    for movie in mathaeser():
        all_movies.append(movie)

    #cinemaxx
    for movie in cm_movie_data:
        all_movies.append(movie)
    for element_movie_playtimes in cm_playtime_data:
        for day in cm_playtime_data[element_movie_playtimes]:
            movie_title = day[0]
            price =  day[1]
            raw_date = day[2]
            for date in day[3]:
                query="""
                INSERT INTO playtimes 
                VALUES (:title, :price, :raw_date, :date)
        
                """
                local_db.execute(query, {"title":movie_title, "price":price, "raw_date":raw_date, "date":date})
                local_c.commit()

            

    for movie_data in all_movies:
        title = movie_data["title"]
        #ptp = str(movie_data["playtime_price"])
        location = movie_data["location"]["name"]
        url = movie_data["location"]["url"]
        #raw_date = movie_data["raw_date"]
        #if current_ptp[0] != ptp:
        query="""
        INSERT INTO movies 
        VALUES (:title, :location, :url)

        """
        local_db.execute(query, {"title":title, "location":location, "url":url, })
        local_c.commit()

if True:
    populate_db()