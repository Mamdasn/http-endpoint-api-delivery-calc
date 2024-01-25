import unittest

import requests
from requests.exceptions import ConnectionError, Timeout

from tests.delivery_fee_test_cases import TestCases


class EndpointTests(unittest.TestCase, TestCases):
    """
    Test the endpoint's connection and query integrity with the API.

    This test class inherits from `TestCases` and focuses on testing
    the HTTP connection to the API and the integrity of query parameters.

    Inherits From:
      | - `TestCases`: A base test class containing logical test cases
           related to delivery fee calculations.

    Test Methods In This Class:
      | - `test_connection`: Test if the HTTP connection to the API is
           available. It sends a valid query to the API and checks if
           the response status code indicates a successful connection.
           It also handles connection errors.

      | - `test_query_integrity`: Test if the HTTP endpoint aborts
           connection when required parameters in the query are not
           satisfied. It sends an invalid query to the API and checks if
           the response status code indicates a rejection due to invalid
           parameters.

    The `check_queries` method is used to check all the queries and their
    expected fees of the inherited test cases with the response of the
    http endpoint.
    """

    http_address = "http://0.0.0.0:5000/delivery_fee"

    def test_connection(self):
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
        query = {
            "no params": True,
        }
        response = requests.post(self.http_address, json=query)

        # Check if the request was aborted
        self.assertTrue(response.status_code == 400, "Invalid query parameters")

    def check_queries(self, queries, expected_delivery_fees):
        for query, expected_delivery_fee in zip(queries, expected_delivery_fees):
            delivery_fee = requests.post(self.http_address, json=query).json()
            self.assertEqual(delivery_fee.get("delivery_fee"), expected_delivery_fee)