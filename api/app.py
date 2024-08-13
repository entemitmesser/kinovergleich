from scrapers.mathaeser_scraper import mScraper
from scrapers.cinemaxx_scraper import cmScraper
from flask import Flask, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='web_interface')
conn = sqlite3.connect("data/movie_data.db")
db = conn.cursor()
mt = mScraper()
cm = cmScraper()

#db setup
try:
    db.execute("DROP TABLE movies")
    db.execute("""CREATE TABLE movies (
            title text,
            playtime_price text,
            location text,
            url text
    )""")
    conn.commit()
    conn.close()
except sqlite3.OperationalError:
    print("Database alrady existent")

@app.route('/')
def index():
    return send_from_directory('web_interface', 'index.html')

@app.route('/movies')
def get_movies():
    all_movies = []

    local_c = sqlite3.connect("data/movie_data.db")
    local_db = local_c.cursor()
    local_db.execute("SELECT * FROM movies")
    list_format_movies = local_db.fetchall()
    for data_block in list_format_movies:
        item = {}
        item["title"] = data_block[0]
        item["playtime_price"] = data_block[1]
        item["location"] = {"name":data_block[2], "url":data_block[3]}
        all_movies.append(item)
    
    return jsonify(all_movies)

@app.route('/titles')
def get_titles():
    local_c = sqlite3.connect("data/movie_data.db")
    local_db = local_c.cursor()
    local_db.execute("SELECT title FROM movies")
    formatted = []
    unformatted = local_db.fetchall()
    for element in unformatted:
        formatted.append(str(element[0]))

    return formatted

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
    for movie in cm.getMovieData():
        movie_data = {}
        movie_data["title"] = movie
        playtime_price_tuples = list(zip(cm.getMovieData()[movie]["playtime"], cm.getMovieData()[movie]["price"]))
        #print(playtime_price_tuples)

        movie_data["playtime_price"] = []

        for tuple in playtime_price_tuples:
            playtime = tuple[0]
            price = cm.getMovieData()[movie]["price"].replace(",", ".")
            movie_data["playtime_price"].append(f"{playtime} +++ {price}\n")

        movie_data["location"] = {"name":"Cinemaxx", "url":"https://www.cinemaxx.de/kinoprogramm/munchen/"}
        movies.append(movie_data)

    return(movies)

def populate_db():

    all_movies = []
    #mathaeser
    for movie in mathaeser():
        all_movies.append(movie)

    #cinemaxx
    for movie in cinemaxx():
        all_movies.append(movie)

    local_c = sqlite3.connect("data/movie_data.db")
    local_db = local_c.cursor()
    local_db.execute(f"SELECT * FROM movies WHERE title=?", (f'{movie}',))

    for movie_data in all_movies:
        title = movie_data["title"]
        ptp = str(movie_data["playtime_price"])
        location = movie_data["location"]["name"]
        url = movie_data["location"]["url"]
        #if current_ptp[0] != ptp:
        query="""
        INSERT INTO movies 
        VALUES (:title, :playtime_price, :location, :url)

        """
        local_db.execute(query, {"title":title, "playtime_price":ptp,"location":location, "url":url})
        local_c.commit()


if __name__ == '__main__':
    populate_db()
    app.run(debug=True)
    