# delivery_tools/__init__.py
# flake8: noqa

"""
This package is designed to facilitate the calculation of delivery fees and ensure
the integrity of delivery-related data. It encompasses a suite of functions that
cater to various aspects of delivery fee computation, taking into account factors
like cart value, delivery distance, item count, and time-specific conditions.

Modules and Functions:
    - delivery_query_integrity_check(data: dict) -> bool:
        Validates the integrity of delivery data. It checks for the presence and
        correct data type of essential fields such as `cart_value`,
        `delivery_distance`, `number_of_items`, and `time`. Returns True if the
        data meets all requirements, otherwise False.

    - calculate_surcharges(cart_value: int, delivery_distance: int,
                           number_of_items: int) -> int:
        Computes additional surcharges for a delivery order based on the cart
        value, delivery distance, and number of items. It applies various criteria
        to calculate these surcharges and returns the total surcharge amount in cents.

    - is_rush_hour(time_str: str) -> bool:
        Determines if a given time falls within the designated rush hour period.
        It checks if the time is within the rush hour window, specifically between
        15:00 and 19:00 on Fridays, and returns True if it does, otherwise False.

    - delivery_fee_calculator(data: dict) -> dict:
        Calculates the total delivery fee for an order. This function integrates
        the `calculate_surcharges` and `is_rush_hour` functions to assess
        additional costs and apply rush hour surcharges. It also considers a base
        delivery fee, applies a maximum cap, and offers free delivery for
        high-value carts. Returns a dictionary with the calculated delivery fee.

Example Usage:
    from delivery_tools.delivery_tools import (
        delivery_fee_calculator,
        delivery_query_integrity_check,
    )
    if delivery_query_integrity_check(order_data):
        fee_info = delivery_fee_calculator(order_data)
        print(f"Delivery Fee: {fee_info['delivery_fee']} cents")
"""


from delivery_tools.delivery_tools import (
    delivery_fee_calculator,
    delivery_query_integrity_check,
)

__all__ = ["delivery_fee_calculator", "delivery_query_integrity_check"]
__version__ = "1.0.0"
