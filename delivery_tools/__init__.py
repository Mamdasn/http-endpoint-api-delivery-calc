# delivery_tools/__init__.py
# flake8: noqa

"""
Package for calculating delivery fees and verifying delivery query integrity.

This package includes utility functions to handle and calculate delivery fees
based on various factors like cart value, delivery distance, number of items,
and specific time considerations. It is designed to provide a robust and
flexible way to apply different rules and surcharges associated with the
delivery of goods.

Modules:
    delivery_tools: Provides functions for checking the integrity of delivery
                    data and calculating delivery fees.

Functions in delivery_tools:
    delivery_query_integrity_check(data: dict) -> bool:
        Checks if the delivery query contains all the required fields with
        appropriate data types. Returns True if the data is valid, False otherwise.

    delivery_fee_calculator(data: dict) -> dict:
        Calculates the delivery fee based on the provided data, considering
        factors like base fee, surcharges for distance and bulk orders, rush
        hour charges, and caps on the maximum fee. Returns a dictionary with
        the calculated fee.

Example Usage:
    from delivery_package import delivery_fee_calculator
    fee_info = delivery_fee_calculator(order_data)
"""

from delivery_tools.delivery_tools import (
    delivery_fee_calculator,
    delivery_query_integrity_check,
)

__all__ = ["delivery_fee_calculator", "delivery_query_integrity_check"]
__version__ = "1.0.0"
