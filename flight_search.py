import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "<API KEY>"

HEADERS = {"apikey": TEQUILA_API_KEY}


class FlightSearch:
    def get_prices(
        self,
        from_iata_code: str,
        to_iata_code: str,
        date_from: str,
        date_to: str,
        nights_from: int,
        nights_to: int,
    ):
        stop_overs = 0

        parameters = {
            "fly_from": from_iata_code,
            "fly_to": to_iata_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": nights_from,
            "nights_in_dst_to": nights_to,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": stop_overs,
            "curr": "USD",
        }

        while stop_overs < 3:
            r = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search", headers=HEADERS, params=parameters
            )
            try:
                data = r.json()["data"][0]
            except IndexError:
                print(
                    f"! No flights found for {to_iata_code} with {stop_overs} layover(s)."
                )
                stop_overs += 1
                parameters["max_stopovers"] = stop_overs
                if stop_overs < 3:
                    print(
                        f"! Finding flights for {to_iata_code} with {stop_overs} layover(s)."
                    )
            else:
                if stop_overs == 0:
                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][0]["cityTo"],
                        destination_airport=data["route"][0]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][1]["local_departure"].split("T")[0],
                    )
                elif stop_overs == 1 and data["route"][0]["flyTo"] != to_iata_code:
                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][1]["cityTo"],
                        destination_airport=data["route"][1]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][2]["local_departure"].split("T")[0],
                        stop_overs=1,
                        via_city_outbound=data["route"][0]["cityTo"],
                    )
                elif stop_overs == 1:
                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][0]["cityTo"],
                        destination_airport=data["route"][0]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][2]["local_departure"].split("T")[0],
                        stop_overs=1,
                        via_city_return=data["route"][1]["cityTo"],
                    )
                elif stop_overs == 2:
                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][1]["cityTo"],
                        destination_airport=data["route"][1]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][2]["local_departure"].split("T")[0],
                        stop_overs=2,
                        via_city_outbound=data["route"][0]["cityTo"],
                        via_city_return=data["route"][2]["cityTo"],
                    )

                print(f"{flight_data.destination_city}: ${flight_data.price}")
                return flight_data
        return None

    def get_iata_code(self, city):
        parameters = {"term": city, "location_types": "city"}

        iata_code = requests.get(
            url=f"{TEQUILA_ENDPOINT}/locations/query",
            headers=HEADERS,
            params=parameters,
        ).json()["locations"][0]["code"]
        return iata_code
