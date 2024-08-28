from flask import jsonify
from lib.str_diff import str_diff
from sqlite3 import Connection

class DatabaseHandler:
    def __init__(self, connection: Connection) -> None:
        self.db_connection = connection
        self.db_cursor = self.db_connection.cursor()

    def get_all_movie_data(self):
        all_movies = []

        self.db_cursor.execute("SELECT * FROM movies")
        list_format_movies = self.db_cursor.fetchall()
        for data_block in list_format_movies:
            item = {"title": data_block[0], "location": {"name": data_block[1], "url_website_cinema": data_block[2]}, "poster_url": data_block[3], "id":data_block[4]}
            playtimes_array = []
            #getting the playtimes from the other table
            self.db_cursor.execute("SELECT raw_date, price FROM playtimes WHERE id=:id", {"id":str(data_block[4])})
            all_query_results = self.db_cursor.fetchall()
            for query_result in all_query_results:
                formatted_element = f'{query_result[0]} +++ {query_result[1]}'

                if formatted_element != 'N/A +++ N/A':
                    try:
                        if formatted_element != playtimes_array[-1]:
                            playtimes_array.append(formatted_element)
                    except IndexError:
                        playtimes_array.append(formatted_element)

            item["playtime_price_formatted_json"] = str(playtimes_array)

            all_movies.append(item)

        return jsonify(all_movies)
    

    def get_movies_by_date(self, date):
        all_movies = []

        self.db_cursor.execute("SELECT * FROM movies WHERE id IN (select id from playtimes where raw_date=:date)", {"date":date})
        list_format_movies = self.db_cursor.fetchall()
        for data_block in list_format_movies:
            item = {"title": data_block[0], "location": {"name": data_block[1], "url_website_cinema": data_block[2]}, "poster_url": data_block[3], "id": data_block[4]}
            playtimes_array = []
            #getting the playtimes from the other table
            self.db_cursor.execute("SELECT * FROM playtimes WHERE id=:id AND raw_date =:date", {"id":str(data_block[4]), "date":date})
            all_query_results = self.db_cursor.fetchall()
            for query_result in all_query_results:
                formatted_element = f'{query_result[3]} +++ {query_result[1]}'
                playtimes_array.append(formatted_element)
            item["playtime_price_formatted_json"] = str(playtimes_array)

            all_movies.append(item)

        return jsonify(all_movies)
    
    def get_movies_by_id(self, mid):
        all_movies = []

        self.db_cursor.execute("SELECT * FROM movies WHERE id IN (select id from playtimes where id=:id)", {"id":mid})
        list_format_movies = self.db_cursor.fetchall()
        for data_block in list_format_movies:
            item = {"title": data_block[0], "location": {"name": data_block[1], "url_website_cinema": data_block[2]}, "poster_url": data_block[3], "id": data_block[4]}
            playtimes_array = []
            #getting the playtimes from the other table
            self.db_cursor.execute("SELECT * FROM playtimes WHERE id=:id AND id =:id", {"id":str(data_block[4]), "id":mid})
            all_query_results = self.db_cursor.fetchall()
            for query_result in all_query_results:
                formatted_element = f'{query_result[3]} +++ {query_result[1]}'
                playtimes_array.append(formatted_element)
            item["playtime_price_formatted_json"] = str(playtimes_array)

            all_movies.append(item)

        return jsonify(all_movies)
    