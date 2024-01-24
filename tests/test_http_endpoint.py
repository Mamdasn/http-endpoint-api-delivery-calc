import unittest

import requests
from requests.exceptions import ConnectionError, Timeout


class EndpointTests(unittest.TestCase):
    http_address = "http://0.0.0.0:5000"

    def test_connection(self):
        """Test if the HTTP connection to the API is available."""
        try:
            query = {
                "cart_value": 890,
                "delivery_distance": 1,
                "number_of_items": 1,
                "time": "2024-01-15T13:00:00Z",
            }
            response = requests.post(self.http_address, json=query)
            # Check if the request was successful
            self.assertTrue(
                response.status_code == 200, "Internet connection available."
            )
        except (ConnectionError, Timeout):
            self.fail("No internet connection.")

    def test_query_integrity(self):
        """Test if the HTTP endpoint aborts connection when required parameters in the query are not satisfied."""
        query = {
            "no params": True,
        }
        response = requests.post(self.http_address, json=query)

        # Check if the request was aborted
        self.assertTrue(response.status_code == 400, "Invalid query parameters")

    def test_fill_10_euro_gap_in_cart_value(self):
        """Test the surcharge calculation for cart values less than 10€."""
        queries = (
            {
                "cart_value": 890,
                "delivery_distance": 1,
                "number_of_items": 1,
                "time": "2024-01-15T13:00:00Z",
            },
        )
        expected_delivery_fees = (310,)
        self.check_delivery_fee(queries, expected_delivery_fees)

    def test_excess_500m_fee(self):
        """Test additional delivery fees for every 500 meters beyond the first 1000 meters."""
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

        self.check_delivery_fee(queries, expected_delivery_fees)

    def test_excess_bulk_fee(self):
        """Test the surcharge for bulk orders based on the number of items in the cart."""
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

        self.check_delivery_fee(queries, expected_delivery_fees)

    def test_15_euro_cap(self):
        """Test the maximum delivery fee cap of 15€, including surcharges."""
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

        self.check_delivery_fee(queries, expected_delivery_fees)

    def test_200_euro_free_delivery(self):
        """Test free delivery for cart values equal to or exceeding 200€."""
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

        self.check_delivery_fee(queries, expected_delivery_fees)

    def test_friday_rush(self):
        """Test increased delivery fees during the Friday rush hours (3 - 7 PM UTC)."""
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

        self.check_delivery_fee(queries, expected_delivery_fees)

    def check_delivery_fee(self, queries, expected_delivery_fees):
        """Test all the queries and expected fees with the http response."""
        for query, expected_delivery_fee in zip(queries, expected_delivery_fees):
            delivery_fee = requests.post(self.http_address, json=query).json()
            self.assertEqual(delivery_fee.get("delivery_fee"), expected_delivery_fee)
