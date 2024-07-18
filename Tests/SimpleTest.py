import datetime
import unittest
import Solution as Solution
from Business.Dish import Dish
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

    def test_basic_order(self) -> None:
        o1 = Order(1, datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time()))
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1))
        o2 = Solution.get_order(o1.get_order_id())
        self.assertEqual(o1.get_datetime(), o2.get_datetime())

    def test_basic_dish(self) -> None:
        d1 = Dish(1, "testDish", 1042.42023, False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        d2 = Solution.get_dish(d1.get_dish_id())
        self.assertEqual(d1.get_name(), d2.get_name())
        self.assertEqual(d1.get_price(), d2.get_price())
        self.assertEqual(d1.get_is_active(), d2.get_is_active())

    def test_basic_update_dish_price(self) -> None:
        d1 = Dish(1, "testDish", 1042.42023, False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1, 3.141))
        d2 = Solution.get_dish(d1.get_dish_id())
        self.assertEqual(d1.get_name(), d2.get_name())
        self.assertEqual(3.141, d2.get_price())
        self.assertEqual(d1.get_is_active(), d2.get_is_active())

    def test_basic_update_dish_is_active(self) -> None:
        d1 = Dish(1, "testDish", 1042.42023, False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(1, True))
        d2 = Solution.get_dish(d1.get_dish_id())
        self.assertEqual(d1.get_name(), d2.get_name())
        self.assertEqual(d1.get_price(), d2.get_price())
        self.assertEqual(True, d2.get_is_active())

    def test_basic_get_all_order_items(self) -> None:
        self.assertEqual([], Solution.get_all_order_items(1))
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        o1 = Order(1, datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time()))
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1))
        d1 = Dish(1, "testDish", 1042.42023, False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))

        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(c1.get_cust_id(), o1.get_order_id()))
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(o1.get_order_id(), d1.get_dish_id(), 20))
        d2 = Solution.get_all_order_items(1)[0]
        self.assertEqual(d2.get_price(), d1.get_price())
        self.assertEqual(d2.get_dish_id(), d1.get_dish_id())
        self.assertEqual(d2.get_amount(), 20)

    def test_basic_customer_likes_dislikes(self) -> None:
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        d1 = Dish(1, "testDish", 1042.42023, False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(c1.get_cust_id(), d1.get_dish_id()))
        self.assertEqual(ReturnValue.OK, Solution.customer_dislike_dish(c1.get_cust_id(), d1.get_dish_id()))
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(c1.get_cust_id(), d1.get_dish_id()))

    def test_basic_get_all_customer_likes(self) -> None:
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        d1 = Dish(1, "testDish", 1042.42023, False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(c1.get_cust_id(), d1.get_dish_id()))
        self.assertEqual([d1], Solution.get_all_customer_likes(c1.get_cust_id()))


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
