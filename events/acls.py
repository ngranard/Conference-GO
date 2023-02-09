import requests
import json

def get_photo(city, state):
    response = requests.get("https://api.pexels.com/v1/search")
    photos = json.loads(response.content)

    photo = {
    "name": photos[""]
    "city": location's city,
    "room_count": the number of rooms available,
    "created": the date/time when the record was created,
    "updated": the date/time when the record was updated,
    "state": the two-letter abbreviation for the state,
    "picture_url": URL of a picture of the city,
}


def get_weather_data(city, state):

