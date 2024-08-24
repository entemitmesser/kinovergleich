#!/Users/moritzruttkowski/Mucino/.venv/bin/python3
from scrapers.mathaeser_scraper import mScraper
from scrapers.cinemaxx_scraper import cmScraper
from datetime import datetime
import sqlite3
import os

mt = mScraper()
cm = cmScraper()
id_counter: int = 0
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
        url text,
        poster_url text,
        id integer
)""")
db.execute("""CREATE TABLE playtimes (
        title text,
        price text,
        raw_date text,
        date text,
        id integer   
)""")
conn.commit()
conn.close()

def mathaeser():
    global id_counter
    movies = []
    playtime_data = {} #Structure: {title: [[title, price, raw_date, date], ...]}
    for movie in mt.getAllMovies():
        movie_data = {}
        movie_data["title"] = movie
        movie_data["poster_url"] = mt.findPosterForMovies()[movie]
        movie_data["id"] = id_counter #placeholder
        playtime_data[movie] = []
        playtime_price_tuples = list(zip(mt.findDatesForMovies()[movie], mt.findPriceForMovies()[movie]))

        for index, (item, price) in enumerate(playtime_price_tuples):
            data_row: list = []
            playtime = item[4:] + "2024"
            try:
                playtime_Date_object = datetime.strptime(str(playtime), " %d.%m.%Y")
                date = playtime_Date_object.strftime("%a %d.%m")
                raw_date = playtime_Date_object.strftime("%d-%m-%Y")
                data_row.extend([movie, price, raw_date, date, id_counter])
            except:
                data_row.extend([movie, "N/A", "N/A", "N/A", id_counter])
            playtime_data[movie].append(data_row)

        movie_data["location"] = {"name":"Mathäser Filmpalast", "url":"https://www.mathaeser.de/mm/"}
        movies.append(movie_data)
        id_counter += 1

    return(movies, playtime_data)

def cinemaxx():
    movies = []
    global id_counter
    movie_table_data, playtime_data = cm.getMovieData()
    for movie in movie_table_data:
        movie_data = {}
        movie_data["title"] = movie
        movie_data["poster_url"] = movie_table_data[movie]["poster"]
        movie_data["id"] = id_counter

        for playtime_data_row in playtime_data[movie]:
            playtime_data_row.append(id_counter)


        movie_data["location"] = {"name":"Cinemaxx", "url":"https://www.cinemaxx.de/kinoprogramm/munchen/"}
        movies.append(movie_data)
        id_counter += 1

    return(movies, playtime_data)

def populate_db():
    cm_movie_data, cm_playtime_data = cinemaxx()
    mt_movie_data, mt_playtime_data = mathaeser()
    all_movies = []
    local_c = sqlite3.connect("data/movie_data.db")
    local_db = local_c.cursor()
    #local_db.execute(f"SELECT * FROM movies WHERE title=?", (f'{movie}',))
    #mathaeser

    #cinemaxx
    for movie in cm_movie_data:
        all_movies.append(movie)
    for element_movie_playtimes in cm_playtime_data:
        for day in cm_playtime_data[element_movie_playtimes]:
            movie_title = day[0]
            price =  day[1]
            raw_date = day[2]
            id = day[4]
            for date in day[3]:
                query="""
                INSERT INTO playtimes 
                VALUES (:title, :price, :raw_date, :date, :id)
        
                """
                local_db.execute(query, {"title":movie_title, "price":price, "raw_date":raw_date, "date":date, "id":id})
                local_c.commit()

    #mathäser
    for movie in mt_movie_data:
        all_movies.append(movie)
    for element_movie_playtimes in mt_playtime_data:
        for day in mt_playtime_data[element_movie_playtimes]:
            movie_title = day[0]
            price =  day[1]
            raw_date = day[2]
            date = day[3]
            id = day[4]
            query="""
            INSERT INTO playtimes 
            VALUES (:title, :price, :raw_date, :date, :id)
    
            """
            local_db.execute(query, {"title":movie_title, "price":price, "raw_date":raw_date, "date":date, "id":id})
            local_c.commit()

            
    for movie_data in all_movies:
        title = movie_data["title"]
        poster_url = str(movie_data["poster_url"])
        id = movie_data["id"]
        #ptp = str(movie_data["playtime_price"])
        location = movie_data["location"]["name"]
        url = movie_data["location"]["url"]
        #raw_date = movie_data["raw_date"]
        #if current_ptp[0] != ptp:
        query="""
        INSERT INTO movies 
        VALUES (:title, :location, :url, :poster_url, :id)

        """
        local_db.execute(query, {"title":title, "location":location, "url":url, "poster_url": poster_url, "id":id})
        local_c.commit()

if True:
    populate_db()