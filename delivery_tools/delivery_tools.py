import math
import datetime


def delivery_data_integrity_check(data):
    keys_to_check = ["cart_value", "delivery_distance", "number_of_items", "time"]
    return all(data.get(key, False) for key in keys_to_check)


def delivery_fee_calculator(data):
    cart_value = data.get("cart_value")
    delivery_distance = data.get("delivery_distance")
    number_of_items = data.get("number_of_items")
    time = data.get("time")

    if cart_value >= 20000:
        return {"delivery_fee": 0}

    surcharge = 0
    # Base fee
    delivery_fee = 200

    # Fill the 10 Euro gap
    if cart_value < 1000:
        surcharge = 1000 - cart_value

    # Increase the delivery fee for each excess 0.5km above the first 1km
    if delivery_distance > 1000:
        surcharge += math.ceil((delivery_distance - 1000) / 500) * 100

    # Add bulk fee per item for no. items more than 5
    if number_of_items >= 5:
        surcharge += (number_of_items - 4) * 50
    # Add an extra bulk fee for no. items more than 12
    if number_of_items > 12:
        surcharge += 120

    delivery_fee += surcharge

    # Convert ISO 8601 formatted timestamp to UTC formatted timestamp
    datetime_utc = datetime.datetime.fromisoformat(time.replace("Z", "+00:00"))

    # Increse the fee by 20% for the Friday rush hour
    day, hour = datetime_utc.strftime("%A"), int(datetime_utc.strftime("%H"))
    if (day == "Friday") and (15 <= hour <= 19):
        delivery_fee *= 1.2

    # Set the delivery fee to 15 Euro cap if the fee exceeds it
    if delivery_fee > 1500:
        delivery_fee = 1500

    return {"delivery_fee": delivery_fee}
