import datetime
import math


def delivery_query_integrity_check(data: dict) -> bool:
    """
    Verifies the integrity of delivery data by checking the presence
    and type of required fields.

    This function examines the provided `data` dictionary to ensure
    it contains all necessary keys: `cart_value`,
    `delivery_distance`, `number_of_items`, and `time`.

    Additionally, it checks that `cart_value`, `delivery_distance`,
    and `number_of_items` are integers, and `time` is a string.
    It returns `True` if all criteria are met, otherwise `False`.

    :param dict data: The order data to be validated. It should be
                      a dictionary with keys corresponding to the
                      required fields.

    :return: A boolean indicating whether the data passes the
             integrity checks. `True` if it does, `False` otherwise.
    :rtype: bool
    """

    keys_to_check = (
        "cart_value",
        "delivery_distance",
        "number_of_items",
        "time",
    )

    keys_with_int_values = ("cart_value", "delivery_distance", "number_of_items")
    check_int_keys = all(isinstance(data.get(key), int) for key in keys_with_int_values)
    check_str_key = isinstance(data.get("time"), str)
    check_keys_existence = all(
        data.get(key, False) is not False for key in keys_to_check
    )

    return check_keys_existence and check_str_key and check_int_keys


def calculate_surcharges(
    cart_value: int, delivery_distance: int, number_of_items: int
) -> int:
    """
    Calculate additional surcharges for a delivery order based on
    cart value, delivery distance, and number of items.

    This function computes surcharges based on several criteria:
        | - A surcharge is added to fill the gap if the cart value is
            below a base fee cap.
        | - Additional surcharges are applied for delivery distances
            exceeding certain thresholds.
        | - Bulk item surcharges are added based on the number of
            items, with higher surcharges for larger quantities.

    :param cart_value: The total value of the cart in cents.
    :type cart_value: int

    :param delivery_distance: The delivery distance in meters.
    :type delivery_distance: int

    :param number_of_items: The number of items in the order.
    :type number_of_items: int

    :return: The total surcharge amount in cents.
    :rtype: int
    """
    surcharge = 0

    BASE_FEE_CAP = 1000
    DISTANCE_THRESHOLD = 1000
    EXTRA_DISTANCE_THRESHOLD = 500
    EXTRA_DISTANCE_SURCHARGE = 100
    BULK_ITEM_THRESHOLD = 5
    BULK_ITEM_SURCHARGE = 50
    EXTRA_BULK_THRESHOLD = 12
    EXTRA_BULK_SURCHARGE = 120

    # Fill the BASE_FEE_CAP gap
    if cart_value < BASE_FEE_CAP:
        surcharge += BASE_FEE_CAP - cart_value

    # Increase the delivery fee for excesses of EXTRA_DISTANCE_THRESHOLD
    # above the first DISTANCE_THRESHOLD
    if delivery_distance > DISTANCE_THRESHOLD:
        excess_distance = delivery_distance - DISTANCE_THRESHOLD
        surcharge += (
            math.ceil(excess_distance / EXTRA_DISTANCE_THRESHOLD)
            * EXTRA_DISTANCE_SURCHARGE
        )

    # Add bulk fee per item for no. items more than equal BULK_ITEM_THRESHOLD
    if number_of_items >= BULK_ITEM_THRESHOLD:
        surcharge += (number_of_items - BULK_ITEM_THRESHOLD + 1) * BULK_ITEM_SURCHARGE

    # Add an extra bulk fee for no. items more than EXTRA_BULK_THRESHOLD
    if number_of_items > EXTRA_BULK_THRESHOLD:
        surcharge += EXTRA_BULK_SURCHARGE

    return surcharge


def is_rush_hour(time_str: str) -> bool:
    """
    Determine whether a given time falls within the designated rush
    hour period.

    This function checks if the specified time is within the rush
    hour window on a specific day of the week.

    Rush hour details:
        | - Rush hour is defined as being between 15:00 and 19:00
            (inclusive) on Fridays.
        | - The time is evaluated in UTC.

    :param time_str: The time in ISO 8601 format string, assumed to
                     be in UTC.
    :type time_str: str

    :return: True if the time is within the rush hour period, False
             otherwise.
    :rtype: bool
    """
    datetime_utc = datetime.datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    day, hour = datetime_utc.strftime("%A"), int(datetime_utc.strftime("%H"))
    return day == "Friday" and 15 <= hour <= 19


def delivery_fee_calculator(data: dict) -> dict:
    """
    Calculate the total delivery fee for an order, incorporating
    various surcharges and special conditions.

    This function integrates multiple components to calculate the
    final delivery fee.

    Used Methods:
        | - It leverages the `calculate_surcharges` function to
            assess additional costs based on cart value, delivery
            distance, and item count.
        | - Utilizes the `is_rush_hour` function to identify and
            apply a surcharge for deliveries during rush hour
            periods.

    The calculation process involves:
        | - Determining if the order qualifies for free delivery
            based on cart value.
        | - Calculating surcharges for distance and bulk items.
        | - Applying a rush hour surcharge if applicable.
        | - Ensuring the total delivery fee does not exceed the
            maximum cap.

    :param data: The order data containing `cart_value` (int),
                 `delivery_distance` (int),
                 `number_of_items` (int), and `time` (ISO 8601
                 format string).
    :type data: dict

    :return: A dictionary with a single key 'delivery_fee' and its
             calculated value in cents.
    :rtype: dict
    """
    cart_value = data.get("cart_value")
    delivery_distance = data.get("delivery_distance")
    number_of_items = data.get("number_of_items")
    time = data.get("time")

    FREE_DELIVERY_CAP = 20000
    BASE_DELIVERY_FEE = 200
    MAX_DELIVERY_FEE = 1500
    RUSH_HOUR_SURCHARGE_RATE = 1.2

    # Make the delivery for free if cart value is higher that 200 euros
    if cart_value >= FREE_DELIVERY_CAP:
        return {"delivery_fee": 0}

    surcharge = calculate_surcharges(cart_value, delivery_distance, number_of_items)
    # Add in the BASE_DELIVERY_FEE to delivery_fee
    delivery_fee = BASE_DELIVERY_FEE + surcharge

    # Increse the fee by 20% for Friday rush hours (15-19)
    if is_rush_hour(time):
        delivery_fee *= RUSH_HOUR_SURCHARGE_RATE

    delivery_fee = int(min(delivery_fee, MAX_DELIVERY_FEE))
    return {"delivery_fee": delivery_fee}
