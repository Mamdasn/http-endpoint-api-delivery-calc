import unittest

from delivery_tools import delivery_fee_calculator


class FeeLogicTests(unittest.TestCase):
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
        """Test additional delivery fees for every 500 meters beyond
        the first 1000 meters."""
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
        """Test the surcharge for bulk orders based on the number
        of items in the cart."""
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
        """Test increased delivery fees during the Friday rush
        hours (3 - 7 PM UTC)."""
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
        """Test all the queries and expected fees with the
        delivery fee calculator library."""
        for query, expected_delivery_fee in zip(queries, expected_delivery_fees):
            delivery_fee = delivery_fee_calculator(query)
            self.assertEqual(delivery_fee.get("delivery_fee"), expected_delivery_fee)