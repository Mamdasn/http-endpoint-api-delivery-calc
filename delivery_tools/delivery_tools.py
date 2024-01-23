import datetime
import math


def delivery_data_integrity_check(data):
    """
    Check the integrity of delivery data.

    This function ensures that all required fields (`cart_value`, `delivery_distance`,
    `number_of_items`, `time`) are present in the data. It returns `True` if all
    fields are present, `False` otherwise.

    :param data: The order data to be checked.
    :type data: dict

    :return: `True` if all required fields are present, `False` otherwise.
    :rtype: bool
    """
    keys_to_check = [
        "cart_value",
        "delivery_distance",
        "number_of_items",
        "time",
    ]
    return all(data.get(key, False) for key in keys_to_check)


def delivery_fee_calculator(data):
    """
    Calculate the delivery fee based on cart value, delivery distance, number
    of items, and time.

    The fee is calculated considering various factors:
        | - Base fee and surcharges for orders below a minimum cart value.
        | - Additional fees for delivery distances beyond a base distance.
        | - Bulk order surcharges based on the number of items.
        | - Special surcharge for Friday rush hours.
        | - Maximum cap on the delivery fee and free delivery for high-value carts.

    :param data: The order data containing `cart_value` (int), `delivery_distance` (int),
                 `number_of_items` (int), and `time` (ISO 8601 format string).
    :type data: dict

    :return: A dictionary with a single key 'delivery_fee' and its calculated value in cents.
    :rtype: dict
    """
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
