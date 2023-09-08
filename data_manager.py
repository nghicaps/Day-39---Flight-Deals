import requests

SHEET_ENDPOINT = "https://api.sheety.co/<sheet>/flightDeals/prices"
TOKEN = "Bearer <TOKEN>"
SHEET_HEADERS = {"Authorization": TOKEN}


class DataManager:
    def __init__(self):
        self.sheet_data = {}

    def get_data(self):
        self.sheet_data = requests.get(
            url=SHEET_ENDPOINT, headers=SHEET_HEADERS
        ).json()["prices"]
        return self.sheet_data

    def update_aita_codes(self):
        for city in self.sheet_data:
            new_data = {"price": {"iataCode": city["iataCode"]}}
            requests.put(
                url=f"{SHEET_ENDPOINT}/{city['id']}",
                headers=SHEET_HEADERS,
                json=new_data,
            )
