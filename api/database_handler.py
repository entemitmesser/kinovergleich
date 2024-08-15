import sqlite3
from flask import jsonify

class databaseHandler():
    def __init__(self, connection) -> None:
        self.db_connection = connection
        self.db_cursor = self.db_connection.cursor()

    def get_all_movie_data(self):
        all_movies = []

        self.db_cursor.execute("SELECT * FROM movies")
        list_format_movies = self.db_cursor.fetchall()
        for data_block in list_format_movies:
            print(data_block[0])
            item = {}
            item["title"] = data_block[0]
            item["location"] = {"name":data_block[1], "url":data_block[2]}
            playtimes_array = []
            #getting the playtimes from the other table
            self.db_cursor.execute("SELECT * FROM playtimes WHERE title=:title", {"title":str(data_block[0])})
            all_query_results = self.db_cursor.fetchall()
            for query_result in all_query_results:
                formatted_element = f'{query_result[3]} +++ {query_result[1]}'
                playtimes_array.append(formatted_element)
            item["playtime_price"] = str(playtimes_array)

            all_movies.append(item)

        return jsonify(all_movies)
    

    def get_movies_by_date(self, date):
        all_movies = []

        self.db_cursor.execute("SELECT * FROM movies WHERE title = (select title from playtimes where raw_date=:date)", {"date":date})
        list_format_movies = self.db_cursor.fetchall()
        for data_block in list_format_movies:
            print(data_block[0])
            item = {}
            item["title"] = data_block[0]
            item["location"] = {"name":data_block[1], "url":data_block[2]}
            playtimes_array = []
            #getting the playtimes from the other table
            self.db_cursor.execute("SELECT * FROM playtimes WHERE title=:title", {"title":str(data_block[0])})
            all_query_results = self.db_cursor.fetchall()
            for query_result in all_query_results:
                formatted_element = f'{query_result[3]} +++ {query_result[1]}'
                playtimes_array.append(formatted_element)
            item["playtime_price"] = str(playtimes_array)

            all_movies.append(item)

        return jsonify(all_movies)