# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_data()

flight_search = FlightSearch()
notification_manager = NotificationManager()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])

    data_manager.sheet_data = sheet_data
    data_manager.update_aita_codes()

tomorrow = (datetime.now() + timedelta(1)).date().strftime("%d/%m/%Y")
six_months = (datetime.now() + timedelta(180)).date().strftime("%d/%m/%Y")

for row in sheet_data:
    flight = flight_search.get_prices(
        from_iata_code="SEA",
        to_iata_code=row["iataCode"],
        date_from=tomorrow,
        date_to=six_months,
        nights_from=7,
        nights_to=28,
    )

    if flight != None and flight.price < row["lowestPrice"]:
        message = f"\nLow Flight Price: ${flight.price}\n{flight.origin_city}({flight.origin_airport}) > {flight.destination_city}({flight.destination_airport})\n{flight.out_date} to {flight.return_date}."

        if flight.stop_overs == 1 and flight.via_city_outbound:
            message += f"\n{flight.stop_overs} outbound layover, via {flight.via_city_outbound}"
        elif flight.stop_overs == 1 and flight.via_city_return:
            message += (
                f"\n{flight.stop_overs} return layover, via {flight.via_city_return}"
            )
        elif flight.stop_overs == 2:
            message += f"\n{flight.stop_overs} layovers,\nvia {flight.via_city_outbound} outbound,\nvia {flight.via_city_return} return"

        notification_manager.send_text(message)
