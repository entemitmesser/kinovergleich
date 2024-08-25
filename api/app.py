from database_handler import DatabaseHandler
from flask import Flask, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='web_interface')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/movies')
def get_movies():
    date_arg_value = request.args.get("date")

    if not date_arg_value:
        conn = sqlite3.connect("data/movie_data.db")
        db_handler = DatabaseHandler(conn)
        return db_handler.get_all_movie_data()
    else:
        conn = sqlite3.connect("data/movie_data.db")
        db_handler = DatabaseHandler(conn)
        return db_handler.get_movies_by_date(date_arg_value)

@app.route('/movie')
def get_movie_by_id():
    id_arg = request.args.get("id")

    if not id_arg:
        return 'Error 400: Bad Request. Try changing the id parameter to a valid value', 400
    else:
        conn = sqlite3.connect("data/movie_data.db")
        db_handler = DatabaseHandler(conn)
        return db_handler.get_movies_by_id(id_arg)

@app.route('/teekessel')
def easteregg():
    return "Check The console for further information", 418

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

if __name__ == '__main__':
    app.run(debug=True)