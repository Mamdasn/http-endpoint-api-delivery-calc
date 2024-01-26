class DeliveryFeeEdgeCases:
    """
    Test cases for the logic of the delivery fee calculations.

    This class contains multiple test cases to verify the results
    of the delivery fee calculations. It covers various scenarios, including
    cart value surcharges, distance-based fees, bulk order surcharges,
    maximum fee caps, and special time-based fees.

    Test Cases:
      | - `test_fill_10_euro_gap_in_cart_value`: Test cases of surcharge
           calculation for cart values less than 10€.
      | - `test_excess_500m_fee`: Test cases of additional delivery fees
           for every 500 meters beyond the first 1000 meters.
      | - `test_excess_bulk_fee`: Test cases of the surcharge for bulk
           orders based on the number of items in the cart.
      | - `test_15_euro_cap`: Test cases of the maximum delivery fee cap
           of 15€, including surcharges.
      | - `test_200_euro_free_delivery`: Test cases of free delivery
           for cart values equal to or exceeding 200€.
      | - `test_friday_rush`: Test cases of increased delivery fees during
           the Friday rush hours (3 - 7 PM UTC).
    """

    def test_fill_10_euro_gap_in_cart_value(self):
        queries = (
            {
                "cart_value": 890,
                "delivery_distance": 1,
                "number_of_items": 1,
                "time": "2024-01-15T13:00:00Z",
            },
            {
                "cart_value": 1000,
                "delivery_distance": 1,
                "number_of_items": 1,
                "time": "2024-01-15T13:00:00Z",
            },
        )
        expected_delivery_fees = (310, 200)
        self.check_queries(queries, expected_delivery_fees)

    def test_excess_500m_fee(self):
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

        self.check_queries(queries, expected_delivery_fees)

    def test_excess_bulk_fee(self):
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
                "number_of_items": 12,
                "time": "2024-01-15T13:00:00Z",
            },
            {
                "cart_value": 1000,
                "delivery_distance": 1000,
                "number_of_items": 13,
                "time": "2024-01-15T13:00:00Z",
            },
        )
        expected_delivery_fees = (200, 250, 600, 770)

        self.check_queries(queries, expected_delivery_fees)

    def test_15_euro_cap(self):
        queries = (
            {
                "cart_value": 1000,
                "delivery_distance": 7000,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            {
                "cart_value": 1000,
                "delivery_distance": 8000,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
        )
        expected_delivery_fees = (1400, 1500)

        self.check_queries(queries, expected_delivery_fees)

    def test_200_euro_free_delivery(self):
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

        self.check_queries(queries, expected_delivery_fees)

    def test_friday_rush(self):
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
        self.check_queries(queries, expected_delivery_fees)

    def check_queries(self, queries: tuple, expected_delivery_fees: tuple):
        return queries, expected_delivery_fees
