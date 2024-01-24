import requests
from requests.exceptions import ConnectionError, Timeout
from test_delivery_fee_logic import FeeLogicTests


class EndpointTests(FeeLogicTests):
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

    def check_delivery_fee(self, queries, expected_delivery_fees):
        """Test all the queries and expected fees with the http response."""
        for query, expected_delivery_fee in zip(queries, expected_delivery_fees):
            delivery_fee = requests.post(self.http_address, json=query).json()
            self.assertEqual(delivery_fee.get("delivery_fee"), expected_delivery_fee)
