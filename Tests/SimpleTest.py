import datetime
import unittest
import Solution as Solution
from Business.Dish import Dish, BadDish
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''


def basicCustomer():
    return Customer(1, 'name', "0502220000", "Haifa")


def basicOrder():
    return Order(1, datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time()))


def basicDish():
    return Dish(1, "testDish", 1042.42023, False)


def assertCustomersEqual(assertThat, customer1, customer2) -> None:
    assertThat(customer1.get_cust_id(), customer2.get_cust_id())
    assertThat(customer1.get_phone(), customer2.get_phone())
    assertThat(customer1.get_address(), customer2.get_address())
    assertThat(customer1.get_full_name(), customer2.get_full_name())


def assertOrdersEqual(assertThat, order1, order2) -> None:
    assertThat(order1.get_order_id(), order2.get_order_id())
    assertThat(order1.get_datetime(), order2.get_datetime())


def assertDishesEqual(assertThat, dish1, dish2) -> None:
    assertThat(dish1.get_name(), dish2.get_name())
    assertThat(dish1.get_price(), dish2.get_price())
    assertThat(dish1.get_is_active(), dish2.get_is_active())


class Test(AbstractTest):
    def test_customer(self) -> None:
        c1 = basicCustomer()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        c2 = Customer(2, None, "0502220000", "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'invalid name')

    def test_basic_order(self) -> None:
        o1 = basicOrder()
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1))
        o2 = Solution.get_order(o1.get_order_id())
        self.assertEqual(o1.get_datetime(), o2.get_datetime())

    def test_basic_dish(self) -> None:
        d1 = basicDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        d2 = Solution.get_dish(d1.get_dish_id())
        self.assertEqual(d1.get_name(), d2.get_name())
        self.assertEqual(d1.get_price(), d2.get_price())
        self.assertEqual(d1.get_is_active(), d2.get_is_active())

    def test_basic_update_dish_price(self) -> None:
        d1 = basicDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1, 3.141))
        d2 = Solution.get_dish(d1.get_dish_id())
        self.assertEqual(d1.get_name(), d2.get_name())
        self.assertEqual(3.141, d2.get_price())
        self.assertEqual(d1.get_is_active(), d2.get_is_active())

    def test_basic_update_dish_is_active(self) -> None:
        d1 = basicDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(1, True))
        d2 = Solution.get_dish(d1.get_dish_id())
        self.assertEqual(d1.get_name(), d2.get_name())
        self.assertEqual(d1.get_price(), d2.get_price())
        self.assertEqual(True, d2.get_is_active())

    def test_basic_order_with_items(self) -> None:
        self.assertEqual([], Solution.get_all_order_items(1))
        c1 = basicCustomer()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        o1 = basicOrder()
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1))
        d1 = basicDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))

        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(c1.get_cust_id(), o1.get_order_id()))
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(o1.get_order_id(), d1.get_dish_id(), 20))
        d2 = Solution.get_all_order_items(1)[0]
        self.assertEqual(d2.get_price(), d1.get_price())
        self.assertEqual(d2.get_dish_id(), d1.get_dish_id())
        self.assertEqual(d2.get_amount(), 20)

    def test_basic_customer_likes_dislikes(self) -> None:
        c1, d1 = self.customerLikesDish()
        self.assertEqual(ReturnValue.OK, Solution.customer_dislike_dish(c1.get_cust_id(), d1.get_dish_id()))
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(c1.get_cust_id(), d1.get_dish_id()))

    def test_basic_get_all_customer_likes(self) -> None:
        c1, d1 = self.customerLikesDish()
        self.assertEqual([d1], Solution.get_all_customer_likes(c1.get_cust_id()))

    def customerLikesDish(self):
        c1 = basicCustomer()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        d1 = basicDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1))
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(c1.get_cust_id(), d1.get_dish_id()))
        return c1, d1

    def test_cannot_insert_null_to_entities(self) -> None:
        customers = [
            Customer(None, 'name', "0502220000", "Haifa"),
            Customer(1, None, "0502220000", "Haifa"),
            Customer(1, 'name', None, "Haifa"),
            Customer(1, 'name', "0502220000", None),
        ]
        orders = [
            Order(None, datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time())),
            Order(1, None),
        ]
        dishes = [
            Dish(None, "testDish", 1042.42023, False),
            Dish(1, None, 1042.42023, False),
            Dish(1, "21", None, False),
            Dish(1, "21", 1, None),
        ]

        entitiesAndAdders = [
            [customers, Solution.add_customer], [orders, Solution.add_order], [dishes, Solution.add_dish]
        ]

        for entitiesAndAdder in entitiesAndAdders:
            entities, adder = entitiesAndAdder
            for entity in entities:
                self.assertEqual(ReturnValue.BAD_PARAMS, adder(entity))

    def test_ids_are_positive(self) -> None:
        entityAndAdders = [
            [
                Customer(-1, 'name', "0502220000", "Haifa"),
                Solution.add_customer
            ],
            [
                Order(-1, datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time())),
                Solution.add_order
            ],
            [
                Dish(-1, "testDish", 1042.42023, False),
                Solution.add_dish
            ]
        ]
        for entityAndAdder in entityAndAdders:
            entity, adder = entityAndAdder
            self.assertEqual(ReturnValue.BAD_PARAMS, adder(entity))

    def test_customer_address_length(self) -> None:
        badCust = Customer(1, '', "", "TT")
        okCust = Customer(1, '', "", "TTT")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(badCust))
        self.assertEqual(ReturnValue.OK, Solution.add_customer(okCust))

    def test_dish_name_length(self) -> None:
        badDish = Dish(1, "TT", 1, False)
        okDish = Dish(1, "TTT", 1, False)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(badDish))
        self.assertEqual(ReturnValue.OK, Solution.add_dish(okDish))

    def test_dish_price_positive(self) -> None:
        badDish1 = Dish(1, "TTT", -1, False)
        badDish2 = Dish(1, "TTT", 0, False)
        okDish = Dish(1, "TTT", 1, False)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(badDish1))
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(badDish2))
        self.assertEqual(ReturnValue.OK, Solution.add_dish(okDish))

    def test_cannot_insert_same_id(self) -> None:
        customers = [
            basicCustomer(),
            Customer(1, "None", "0502220000", "Haifa"),
        ]
        orders = [
            basicOrder(),
            Order(1, datetime.datetime.today()),
        ]
        dishes = [
            Dish(1, "testDish1", 1042.42023, False),
            Dish(1, "testDish2", 1, False),
        ]

        entitiesAndAdders = [
            [customers, Solution.add_customer], [orders, Solution.add_order], [dishes, Solution.add_dish]
        ]

        for entitiesAndAdder in entitiesAndAdders:
            entities, adder = entitiesAndAdder
            self.assertEqual(ReturnValue.OK, adder(entities[0]))
            self.assertEqual(ReturnValue.ALREADY_EXISTS, adder(entities[1]))

    def test_get_not_exists(self) -> None:
        self.assertEqual(Solution.add_customer(basicCustomer()), ReturnValue.OK)
        self.assertEqual(Solution.add_order(basicOrder()), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(basicDish()), ReturnValue.OK)

        shouldBeBadCustomer = Solution.get_customer(basicCustomer().get_cust_id() + 1)
        actualBadCustomer = BadCustomer()
        assertCustomersEqual(self.assertEqual, shouldBeBadCustomer, actualBadCustomer)

        shouldBeBadOrder = Solution.get_order(basicOrder().get_order_id() + 1)
        actualBadOrder = BadOrder()
        assertOrdersEqual(self.assertEqual, shouldBeBadOrder, actualBadOrder)

        shouldBeBadDish = Solution.get_dish(basicDish().get_dish_id() + 1)
        actualBadDish = BadDish()
        assertDishesEqual(self.assertEqual, shouldBeBadDish, actualBadDish)


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
