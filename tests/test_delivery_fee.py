import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from delivery_tools import delivery_fee_calculator


def test_fill_10_euro_gap_in_cart_value():
    query = {
        "cart_value": 890,
        "delivery_distance": 1,
        "number_of_items": 1,
        "time": "2024-01-15T13:00:00Z",
    }
    expected_delivery_fee = 310
    delivery_fee = delivery_fee_calculator(query)
    delivery_fee_value = delivery_fee.get("delivery_fee")
    assert delivery_fee_value == expected_delivery_fee


def test_excess_500m_fee():
    queries = (
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1499,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1500,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1501,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    expected_delivery_fees = (200, 300, 300, 400)

    for expected_delivery_fee, query in zip(expected_delivery_fees, queries):
        delivery_fee = delivery_fee_calculator(query)
        delivery_fee_value = delivery_fee.get("delivery_fee")
        assert delivery_fee_value == expected_delivery_fee


def test_excess_bulk_fee():
    queries = (
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 5,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 10,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 13,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 14,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    expected_delivery_fees = (200, 250, 500, 770, 820)

    for expected_delivery_fee, query in zip(expected_delivery_fees, queries):
        delivery_fee = delivery_fee_calculator(query)
        delivery_fee_value = delivery_fee.get("delivery_fee")
        assert delivery_fee_value == expected_delivery_fee


def test_15_euro_cap():
    queries = (
        {
            "cart_value": 1000,
            "delivery_distance": 7001,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 7001,
            "number_of_items": 12,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    expected_delivery_fees = (1500, 1500)

    for expected_delivery_fee, query in zip(expected_delivery_fees, queries):
        delivery_fee = delivery_fee_calculator(query)
        delivery_fee_value = delivery_fee.get("delivery_fee")
        assert delivery_fee_value == expected_delivery_fee


def test_200_euro_free_delivery():
    queries = (
        {
            "cart_value": 19999,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 20000,
            "delivery_distance": 7001,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    expected_delivery_fees = (200, 0)

    for expected_delivery_fee, query in zip(expected_delivery_fees, queries):
        delivery_fee = delivery_fee_calculator(query)
        delivery_fee_value = delivery_fee.get("delivery_fee")
        assert delivery_fee_value == expected_delivery_fee


def test_friday_rush():
    queries = (
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-19T14:59:59Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-19T15:00:00Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-19T19:00:00Z",
        },
    )
    expected_delivery_fees = (200, 240, 240)

    for expected_delivery_fee, query in zip(expected_delivery_fees, queries):
        delivery_fee = delivery_fee_calculator(query)
        delivery_fee_value = delivery_fee.get("delivery_fee")
        assert delivery_fee_value == expected_delivery_fee
