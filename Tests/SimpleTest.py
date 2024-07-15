import datetime
import unittest
import Solution as Solution
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer
from Business.Order import Order

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''


class Test(AbstractTest):
    def test_customer(self) -> None:
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        c2 = Customer(2, None, "0502220000", "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'invalid name')

    def test_order(self) -> None:
        o1 = Order(1, datetime.datetime.now())
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1))




# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
