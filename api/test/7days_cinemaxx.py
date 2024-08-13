from datetime import datetime, timedelta
import json
import requests

# Set the cinema ID, type, and today's date
cinema_id = 11
type = "jetzt-im-kino"
days_to_fetch = 7

# Create an empty dictionary to store all the data
all_data = {}

# Loop through each day of the coming week
for i in range(days_to_fetch):
    date = datetime.today() + timedelta(days=i)
    date_str = date.strftime("%d-%m-%Y")

    # Fetch data from the API
    api_url = f"https://www.cinemaxx.de/api/sitecore/WhatsOn/WhatsOnV2ByTopfilms?cinemaId={cinema_id}&Datum={date_str}&type={type}"
    response = requests.get(api_url)

    if response.status_code == 200:
        # Convert response to JSON
        data = response.json()

        # Add data to the dictionary using the date as key
        all_data[date_str] = data
    else:
        print(f"Failed to fetch data for {date_str} from the API.")

# Write all the data to a single JSON file
with open("test/cinemaxx_all.json", "w", encoding="utf-8") as json_file:
    json.dump(all_data, json_file)

