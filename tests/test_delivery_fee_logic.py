import unittest

from delivery_tools import delivery_fee_calculator
from tests.delivery_fee_test_cases import DeliveryFeeEdgeCases


class FeeLogicTests(unittest.TestCase, DeliveryFeeEdgeCases):
    """
    This test class inherits from `DeliveryFeeEdgeCases` and focuses on testing
    the logic of the delivery fee calculator package.

    Inherits From:
      | - `DeliveryFeeEdgeCases`: A base test class containing logical test cases
           related to delivery fee calculations.

    The `check_queries` method is used to check all the queries and their
    expected fees of the inherited test cases with the results of delivery
    fee calculator library.
    """

    def check_queries(self, queries: tuple, expected_delivery_fees: tuple):
        for query, expected_delivery_fee in zip(queries, expected_delivery_fees):
            delivery_fee = delivery_fee_calculator(query)
            self.assertEqual(delivery_fee.get("delivery_fee"), expected_delivery_fee)
