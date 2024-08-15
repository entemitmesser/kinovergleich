import requests
import json
from datetime import datetime, timedelta

class cmScraper():
    def __init__(self) -> None:
        self.cinema_id = 11
        self.type = "jetzt-im-kino"
        self.days_to_fetch = 7

        # Create an empty dictionary to store all the data
        self.all_data = {}

        # Loop through each day of the coming week
        for i in range(self.days_to_fetch):
            date = datetime.today() + timedelta(days=i)
            date_str = date.strftime("%d-%m-%Y")

            # Fetch data from the API
            api_url = f"https://www.cinemaxx.de/api/sitecore/WhatsOn/WhatsOnV2ByTopfilms?cinemaId={self.cinema_id}&Datum={date_str}&type={type}"
            response = requests.get(api_url)

            if response.status_code == 200:
                # Convert response to JSON
                data = response.json()

                # Add data to the dictionary using the date as key
                self.all_data[date_str] = data
            else:
                print(f"Failed to fetch data for {date_str} from the API.")

            # Write all the data to a single JSON file
            with open("data/cinemaxx_all.json", "w", encoding="utf-8") as json_file:
                json.dump(self.all_data, json_file)

    def getMovieData(self):
        movie_data = {}
        #Structure: {title: [[title, price, raw_date, date], ...]}
        playtime_data = {}
        with open("data/cinemaxx_all.json", "r") as f:
            data = json.loads(f.read())

        for i in range(self.days_to_fetch):
            date = datetime.today() + timedelta(days=i)
            date_str = date.strftime("%d-%m-%Y")

            # Iterate over each movie entry
            for movie in data[date_str]["WhatsOnAlphabeticFilms"]:
                # Extract movie title
                title = movie["Title"]
                movie_data[title] = {}
                try:
                    playtime_data[title]
                except KeyError:
                    playtime_data[title] = []

                # Iterate over cinemas and schedules
                for cinema in movie["WhatsOnAlphabeticCinemas"]:
                    playtime = []
                    for schedule in cinema["WhatsOnAlphabeticCinemas"][0]["WhatsOnAlphabeticShedules"]:
                        # Extract playtime
                        obj_date = datetime.strptime(schedule["Time"], "%Y-%m-%d %H:%M:%S")
                        pretty_date = obj_date.strftime("%a. %d.%m %H:%M")
                        uniform_date = obj_date.strftime("%d/%m/%Y")
                        playtime.append(pretty_date)
                        #movie_data[title]["playtime"] = playtime
                        #movie_data[title]["price"] = "ab 8,99€"
                        #movie_data[title]["raw_date"] = uniform_date
                        data_block = [
                            title,
                            "ab 8,99€",
                            date_str,
                            playtime
                        ]
                        playtime_data[title].append(data_block)

                        # Extract duration (if available)
                        for param in movie["FilmParams"]:
                            if "Minuten" in param["Title"]:
                                duration = param["Title"]
                                movie_data[title]["duration"] = duration
                                break
                        else:
                            print("Duration not available")

                        #print()  # Print an empty line between schedules
            
        return(movie_data, playtime_data)

#mdata, pdata = cmScraper().getMovieData()
#print(mdata)
#print("\n\n\n\n\n\n\n\n")
#print(pdata)
