import datetime
import unittest
import Solution as Solution
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''


def createCustomer(cust_id=1, full_name='name', phone="0502220000", address="Haifa"):
    return Customer(cust_id, full_name, phone, address)


def createOrder(order_id=1, date=datetime.datetime.now().replace(microsecond=0)):
    return Order(order_id, date)


def createDish(dish_id=1, name="testDish", price=1042.42023, is_active=True):
    return Dish(dish_id, name, price, is_active)


def assertCustomersEqual(assertEqual, customer1, customer2) -> None:
    assertEqual(customer1.get_cust_id(), customer2.get_cust_id())
    assertEqual(customer1.get_phone(), customer2.get_phone())
    assertEqual(customer1.get_address(), customer2.get_address())
    assertEqual(customer1.get_full_name(), customer2.get_full_name())


def assertOrdersEqual(assertEqual, order1, order2) -> None:
    assertEqual(order1.get_order_id(), order2.get_order_id())
    assertEqual(order1.get_datetime(), order2.get_datetime())


def assertDishesEqual(assertEqual, dish1, dish2) -> None:
    assertEqual(dish1.get_name(), dish2.get_name())
    assertEqual(dish1.get_price(), dish2.get_price())
    assertEqual(dish1.get_is_active(), dish2.get_is_active())


def assertOrderDishesEqual(assertEqual, orderDish1, orderDish2) -> None:
    assertEqual(orderDish1.get_dish_id(), orderDish2.get_dish_id())
    assertEqual(orderDish1.get_price(), orderDish2.get_price())
    assertEqual(orderDish1.get_amount(), orderDish2.get_amount())


class Test(AbstractTest):
    # staff test
    def test_customer(self) -> None:
        c1 = createCustomer()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        c2 = Customer(2, None, "0502220000", "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'invalid name')

    def test_basic_order(self) -> None:
        order1 = createOrder()
        self.assertEqual(ReturnValue.OK, Solution.add_order(order1))
        order2 = Solution.get_order(order1.get_order_id())
        assertOrdersEqual(self.assertEqual, order1, order2)

    def test_basic_dish(self) -> None:
        dish1 = createDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish1))
        dish2 = Solution.get_dish(dish1.get_dish_id())
        assertDishesEqual(self.assertEqual, dish1, dish2)

    def test_basic_update_dish_price(self) -> None:
        dish1 = createDish()
        newPrice = 3.141

        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish1))
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(dish1.get_dish_id(), newPrice))

        dish2 = Solution.get_dish(dish1.get_dish_id())
        dish1.set_price(newPrice)
        assertDishesEqual(self.assertEqual, dish1, dish2)

    def test_basic_update_dish_is_active(self) -> None:
        dish1 = createDish()
        newIsActive = True

        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish1))
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(dish1.get_dish_id(), newIsActive))

        dish2 = Solution.get_dish(dish1.get_dish_id())
        dish1.set_is_active(newIsActive)
        assertDishesEqual(self.assertEqual, dish1, dish2)

    def test_basic_order_with_items(self) -> None:
        order, customer = self.customer_placed_order()
        dish1 = createDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish1))
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(order.get_order_id(), dish1.get_dish_id(), 20))
        dish2 = Solution.get_all_order_items(1)[0]
        self.assertEqual(dish2.get_price(), dish1.get_price())
        self.assertEqual(dish2.get_dish_id(), dish1.get_dish_id())
        self.assertEqual(dish2.get_amount(), 20)

    def customer_placed_order(self):
        self.assertEqual([], Solution.get_all_order_items(1))
        customer = createCustomer()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(customer))
        order = createOrder()
        self.assertEqual(ReturnValue.OK, Solution.add_order(order))
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(customer.get_cust_id(), order.get_order_id()))
        return order, customer

    def test_basic_customer_likes_dislikes(self) -> None:
        customer1, dish1 = self.customerLikesDish()
        self.assertEqual(ReturnValue.OK, Solution.customer_dislike_dish(customer1.get_cust_id(), dish1.get_dish_id()))
        self.assertEqual(
            ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(customer1.get_cust_id(), dish1.get_dish_id())
        )

    def test_basic_get_all_customer_likes(self) -> None:
        customer1, dish1 = self.customerLikesDish()
        self.assertEqual([dish1], Solution.get_all_customer_likes(customer1.get_cust_id()))

    def test_basic_get_customer_that_placed_order(self) -> None:
        order, customer = self.customer_placed_order()
        assertCustomersEqual(
            self.assertEqual, customer, Solution.get_customer_that_placed_order(customer.get_cust_id())
        )

    def customerLikesDish(self):
        customer1 = createCustomer()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(customer1), 'regular customer')
        dish1 = createDish()
        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish1))
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(customer1.get_cust_id(), dish1.get_dish_id()))
        return customer1, dish1

    def test_cannot_insert_null_to_entities(self) -> None:
        customers = [
            createCustomer(cust_id=None),
            createCustomer(full_name=None),
            createCustomer(phone=None),
            createCustomer(address=None),
        ]
        orders = [
            createOrder(order_id=None),
            createOrder(date=None),
        ]
        dishes = [
            createDish(dish_id=None),
            createDish(name=None),
            createDish(price=None),
            createDish(is_active=None),
        ]

        entitiesAndAdders = [
            [customers, Solution.add_customer], [orders, Solution.add_order], [dishes, Solution.add_dish]
        ]

        for entitiesAndAdder in entitiesAndAdders:
            entities, adder = entitiesAndAdder
            for entity in entities:
                self.assertEqual(ReturnValue.BAD_PARAMS, adder(entity))

    def test_ids_are_positive(self) -> None:
        entitiesAndAdders = [
            [
                [createCustomer(cust_id=-1), createCustomer(cust_id=0)],
                Solution.add_customer
            ],
            [
                [createOrder(order_id=-1), createOrder(order_id=0)],
                Solution.add_order
            ],
            [
                [createDish(dish_id=-1), createDish(dish_id=0)],
                Solution.add_dish
            ]
        ]
        for entityAndAdder in entitiesAndAdders:
            entities, adder = entityAndAdder
            for entity in entities:
                self.assertEqual(ReturnValue.BAD_PARAMS, adder(entity))

    def test_customer_address_length(self) -> None:
        badCust = createCustomer(address="AA")
        okCust = createCustomer(address="AAA")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(badCust))
        self.assertEqual(ReturnValue.OK, Solution.add_customer(okCust))

    def test_dish_name_length(self) -> None:
        badDish = createDish(name="AA")
        okDish = createDish(name="AAA")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(badDish))
        self.assertEqual(ReturnValue.OK, Solution.add_dish(okDish))

    def test_dish_price_positive(self) -> None:
        badDishes = [createDish(price=-1), createDish(price=0)]
        for badDish in badDishes:
            self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(badDish))

    def test_cannot_insert_same_entity_id(self) -> None:
        customers = [
            createCustomer(),
            createCustomer(full_name="test"),
        ]
        orders = [
            createOrder(),
            createOrder(date=datetime.datetime.today()),
        ]
        dishes = [
            createDish(),
            createDish(price=1),
        ]

        entitiesAndAdders = [
            [customers, Solution.add_customer], [orders, Solution.add_order], [dishes, Solution.add_dish]
        ]

        for entitiesAndAdder in entitiesAndAdders:
            entities, adder = entitiesAndAdder
            self.assertEqual(ReturnValue.OK, adder(entities[0]))
            self.assertEqual(ReturnValue.ALREADY_EXISTS, adder(entities[1]))

    def test_get_not_existing_entities(self) -> None:
        self.assertEqual(Solution.add_customer(createCustomer()), ReturnValue.OK)
        self.assertEqual(Solution.add_order(createOrder()), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(createDish()), ReturnValue.OK)

        shouldBeBadCustomer = Solution.get_customer(createCustomer().get_cust_id() + 1)
        actualBadCustomer = BadCustomer()
        assertCustomersEqual(self.assertEqual, shouldBeBadCustomer, actualBadCustomer)

        shouldBeBadOrder = Solution.get_order(createOrder().get_order_id() + 1)
        actualBadOrder = BadOrder()
        assertOrdersEqual(self.assertEqual, shouldBeBadOrder, actualBadOrder)

        shouldBeBadDish = Solution.get_dish(createDish().get_dish_id() + 1)
        actualBadDish = BadDish()
        assertDishesEqual(self.assertEqual, shouldBeBadDish, actualBadDish)

    def test_basic_delete_entities(self) -> None:
        self.assertEqual(Solution.add_customer(createCustomer()), ReturnValue.OK)
        self.assertEqual(Solution.add_order(createOrder()), ReturnValue.OK)

        self.assertEqual(Solution.delete_customer(createCustomer().get_cust_id()), ReturnValue.OK)
        self.assertEqual(Solution.delete_order(createOrder().get_order_id()), ReturnValue.OK)

        assertCustomersEqual(self.assertEqual, BadCustomer(), Solution.get_customer(createCustomer().get_cust_id()))
        assertOrdersEqual(self.assertEqual, BadOrder(), Solution.get_order(createOrder().get_order_id()))

    def test_delete_not_existing_entities(self) -> None:
        self.assertEqual(Solution.add_customer(createCustomer()), ReturnValue.OK)
        self.assertEqual(Solution.add_order(createOrder()), ReturnValue.OK)

        self.assertEqual(Solution.delete_customer(createCustomer().get_cust_id()+1), ReturnValue.NOT_EXISTS)
        self.assertEqual(Solution.delete_order(createOrder().get_order_id()+1), ReturnValue.NOT_EXISTS)

    def test_make_sure_updated_price_is_positive(self) -> None:
        dish = createDish()
        self.assertEqual(Solution.add_dish(dish), ReturnValue.OK)
        self.assertEqual(Solution.update_dish_price(dish.get_dish_id(), -1), ReturnValue.BAD_PARAMS)
        self.assertEqual(Solution.update_dish_price(dish.get_dish_id(), 0), ReturnValue.BAD_PARAMS)

    def test_update_non_existing_dish(self) -> None:
        dish = createDish()
        self.assertEqual(Solution.add_dish(dish), ReturnValue.OK)

        non_existing_dish_id = dish.get_dish_id() + 1
        self.assertEqual(Solution.update_dish_price(non_existing_dish_id, 1), ReturnValue.NOT_EXISTS)
        self.assertEqual(Solution.update_dish_active_status(non_existing_dish_id, True), ReturnValue.NOT_EXISTS)

    def test_update_price_of_inactive_dish(self) -> None:
        dish = createDish(is_active=False)
        self.assertEqual(Solution.add_dish(dish), ReturnValue.OK)

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_price(dish.get_dish_id(), 432))

    def test_clear_tables(self) -> None:
        customer1 = createCustomer()
        order1 = createOrder()
        dish1 = createDish()

        # insert two records for each table
        self.assertEqual(Solution.add_customer(customer1), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order1), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        self.assertEqual(Solution.customer_placed_order(customer1.get_cust_id(), order1.get_order_id()), ReturnValue.OK)
        self.assertEqual(Solution.order_contains_dish(order1.get_order_id(), dish1.get_dish_id(), 1), ReturnValue.OK)
        self.assertEqual(Solution.customer_likes_dish(customer1.get_cust_id(), dish1.get_dish_id()), ReturnValue.OK)
        secondEntityId = 2
        self.assertEqual(Solution.add_customer(createCustomer(cust_id=secondEntityId)), ReturnValue.OK)
        self.assertEqual(Solution.add_order(createOrder(order_id=secondEntityId)), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(createDish(dish_id=secondEntityId)), ReturnValue.OK)
        self.assertEqual(Solution.customer_placed_order(secondEntityId, secondEntityId), ReturnValue.OK)
        self.assertEqual(Solution.order_contains_dish(secondEntityId, secondEntityId, 1), ReturnValue.OK)
        self.assertEqual(Solution.customer_likes_dish(secondEntityId, secondEntityId), ReturnValue.OK)

        # clear tables
        Solution.clear_tables()

        # make sure all getter APIs do not return a result for given ids
        assertCustomersEqual(self.assertEqual, BadCustomer(), Solution.get_customer(customer1.get_cust_id()))
        assertCustomersEqual(self.assertEqual, BadCustomer(), Solution.get_customer(secondEntityId))
        assertCustomersEqual(self.assertEqual, BadCustomer(), Solution.get_customer_that_placed_order(secondEntityId))
        assertCustomersEqual(
            self.assertEqual, BadCustomer(), Solution.get_customer_that_placed_order(customer1.get_cust_id())
        )
        assertOrdersEqual(self.assertEqual, BadOrder(), Solution.get_order(secondEntityId))
        assertOrdersEqual(self.assertEqual, BadOrder(), Solution.get_order(order1.get_order_id()))
        assertDishesEqual(self.assertEqual, BadDish(), Solution.get_dish(dish1.get_dish_id()))
        assertDishesEqual(self.assertEqual, BadDish(), Solution.get_dish(secondEntityId))
        self.assertEqual([], Solution.get_all_order_items(order1.get_order_id()))
        self.assertEqual([], Solution.get_all_order_items(secondEntityId))
        self.assertEqual([], Solution.get_all_customer_likes(customer1.get_cust_id()))
        self.assertEqual([], Solution.get_all_customer_likes(secondEntityId))

    def test_unique_customer_for_each_order(self) -> None:
        customer = createCustomer()
        order1 = createOrder()
        order2 = createOrder(order_id=2)
        self.assertEqual(Solution.add_customer(customer), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order1), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order2), ReturnValue.OK)

        self.assertEqual(Solution.customer_placed_order(customer.get_cust_id(), order1.get_order_id()), ReturnValue.OK)
        self.assertEqual(Solution.customer_placed_order(customer.get_cust_id(), order2.get_order_id()), ReturnValue.OK)
        self.assertEqual(
            Solution.customer_placed_order(customer.get_cust_id(), order1.get_order_id()), ReturnValue.ALREADY_EXISTS
        )

    def test_non_existing_customer_placed_order(self) -> None:
        customer = createCustomer()
        order = createOrder()
        non_existing_id = 134232

        self.assertEqual(Solution.add_customer(customer), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order), ReturnValue.OK)

        self.assertEqual(
            Solution.customer_placed_order(non_existing_id, order.get_order_id()), ReturnValue.NOT_EXISTS
        )
        self.assertEqual(
            Solution.customer_placed_order(customer.get_cust_id(), non_existing_id), ReturnValue.NOT_EXISTS
        )
        self.assertEqual(
            Solution.customer_placed_order(non_existing_id, non_existing_id), ReturnValue.NOT_EXISTS
        )
        self.assertEqual(Solution.customer_placed_order(customer.get_cust_id(), order.get_order_id()), ReturnValue.OK)

    def test_non_existing_entities_order_contains_dish(self) -> None:
        order1 = createOrder()
        order2 = createOrder(order_id=2)
        dish = createDish()
        non_existing_id = 134232

        self.assertEqual(Solution.add_dish(dish), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order1), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order2), ReturnValue.OK)

        self.assertEqual(
            Solution.order_contains_dish(order1.get_order_id(), non_existing_id, 1), ReturnValue.NOT_EXISTS
        )
        self.assertEqual(Solution.order_contains_dish(non_existing_id, dish.get_dish_id(), 1), ReturnValue.NOT_EXISTS)
        self.assertEqual(Solution.order_contains_dish(non_existing_id, non_existing_id, 1), ReturnValue.NOT_EXISTS)

        self.assertEqual(Solution.update_dish_active_status(dish.get_dish_id(), False), ReturnValue.OK)
        self.assertEqual(
            Solution.order_contains_dish(order2.get_order_id(), dish.get_dish_id(), 1), ReturnValue.NOT_EXISTS
        )

        self.assertEqual(
            Solution.order_does_not_contain_dish(order1.get_order_id(), non_existing_id), ReturnValue.NOT_EXISTS
        )
        self.assertEqual(
            Solution.order_does_not_contain_dish(non_existing_id, dish.get_dish_id()), ReturnValue.NOT_EXISTS
        )
        self.assertEqual(Solution.order_does_not_contain_dish(non_existing_id, non_existing_id), ReturnValue.NOT_EXISTS)

    def test_amount_positive_order_contains_dish(self) -> None:
        order = createOrder()
        dish = createDish()

        self.assertEqual(Solution.add_dish(dish), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order), ReturnValue.OK)

        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish.get_dish_id(), -1), ReturnValue.BAD_PARAMS
        )
        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish.get_dish_id(), 0), ReturnValue.BAD_PARAMS
        )

    def test_unique_order_contains_dish(self) -> None:
        order1 = createOrder()
        order2 = createOrder(order_id=2)
        dish1 = createDish()
        dish2 = createDish(dish_id=2)

        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish2), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order1), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order2), ReturnValue.OK)

        self.assertEqual(
            Solution.order_contains_dish(order1.get_order_id(), dish1.get_dish_id(), 1), ReturnValue.OK
        )
        self.assertEqual(
            Solution.order_contains_dish(order1.get_order_id(), dish1.get_dish_id(), 2), ReturnValue.ALREADY_EXISTS
        )
        self.assertEqual(
            Solution.order_contains_dish(order2.get_order_id(), dish1.get_dish_id(), 1), ReturnValue.OK
        )
        self.assertEqual(
            Solution.order_contains_dish(order1.get_order_id(), dish2.get_dish_id(), 1), ReturnValue.OK
        )

    def test_get_few_order_items(self) -> None:
        order = createOrder()
        dish1 = createDish()
        dish2 = createDish(dish_id=2, name="testDish2", price=2)
        dish3 = createDish(dish_id=3, name="testDish3", price=3)

        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish2), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish3), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order), ReturnValue.OK)

        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish1.get_dish_id(), 1), ReturnValue.OK
        )
        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish2.get_dish_id(), 2), ReturnValue.OK
        )
        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish3.get_dish_id(), 3), ReturnValue.OK
        )

        orderDishes = Solution.get_all_order_items(order.get_order_id())
        assertOrderDishesEqual(self.assertEqual, orderDishes[0], OrderDish(dish1.get_dish_id(), 1, dish1.get_price()))
        assertOrderDishesEqual(self.assertEqual, orderDishes[1], OrderDish(dish2.get_dish_id(), 2, dish2.get_price()))
        assertOrderDishesEqual(self.assertEqual, orderDishes[2], OrderDish(dish3.get_dish_id(), 3, dish3.get_price()))

    def test_get_empty_order_dish(self) -> None:
        order = createOrder()
        self.assertEqual(Solution.add_order(order), ReturnValue.OK)

        self.assertEqual([], Solution.get_all_order_items(23453))
        self.assertEqual([], Solution.get_all_order_items(order.get_order_id()))

    def test_like_already_exists(self) -> None:
        customer1 = createCustomer()
        customer2 = createCustomer(cust_id=2)
        dish1 = createDish()
        dish2 = createDish(dish_id=2)
        self.assertEqual(Solution.add_customer(customer1), ReturnValue.OK)
        self.assertEqual(Solution.add_customer(customer2), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish2), ReturnValue.OK)

        self.insert_like_twice_and_assert_exists(customer1, dish1)
        self.insert_like_twice_and_assert_exists(customer1, dish2)
        self.insert_like_twice_and_assert_exists(customer2, dish1)

    def insert_like_twice_and_assert_exists(self, customer, dish) -> None:
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(customer.get_cust_id(), dish.get_dish_id()))
        self.assertEqual(
            ReturnValue.ALREADY_EXISTS, Solution.customer_likes_dish(customer.get_cust_id(), dish.get_dish_id())
        )

    def test_like_not_existing_entities(self) -> None:
        customer = createCustomer()
        dish = createDish()
        self.assertEqual(Solution.add_customer(customer), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish), ReturnValue.OK)
        non_existing_id = 143785

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(non_existing_id, dish.get_dish_id()))
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(customer.get_cust_id(), non_existing_id))
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(non_existing_id, non_existing_id))

    def test_dislike_without_like_existing(self) -> None:
        customer = createCustomer()
        dish1 = createDish()
        dish2 = createDish(dish_id=2)
        self.assertEqual(Solution.add_customer(customer), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        non_existing_id = 143785

        self.assertEqual(
            ReturnValue.OK, Solution.customer_likes_dish(customer.get_cust_id(), dish1.get_dish_id())
        )
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(non_existing_id, dish1.get_dish_id()))
        self.assertEqual(
            ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(customer.get_cust_id(), non_existing_id)
        )
        self.assertEqual(
            ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(non_existing_id, non_existing_id)
        )
        self.assertEqual(
            ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(customer.get_cust_id(), dish2.get_dish_id())
        )

    def test_few_customer_likes(self) -> None:
        customer = createCustomer()
        dish1 = createDish()
        dish2 = createDish(dish_id=2, name="testDish2", price=2.3)
        dish3 = createDish(dish_id=3, name="testDish3", price=3.4)
        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish2), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish3), ReturnValue.OK)
        self.assertEqual(Solution.add_customer(customer), ReturnValue.OK)
        givenDishes = [dish1, dish2, dish3]

        for dish in givenDishes:
            self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(customer.get_cust_id(), dish.get_dish_id()))

        outputDishes = Solution.get_all_customer_likes(customer.get_cust_id())
        assertDishesEqual(self.assertEqual, outputDishes[0], dish1)
        assertDishesEqual(self.assertEqual, outputDishes[1], dish2)
        assertDishesEqual(self.assertEqual, outputDishes[2], dish3)

    def test_all_likes_not_existing(self) -> None:
        customer = createCustomer()
        self.assertEqual(Solution.add_customer(customer), ReturnValue.OK)

        self.assertEqual([], Solution.get_all_customer_likes(customer.get_cust_id()))
        self.assertEqual([], Solution.get_all_customer_likes(34242))

    def test_get_order_total_price(self) -> None:
        orderId = 1
        expected_price = self.createOrderWithDishes(
            orderId, 1, 2, 3, 1, 2, 3
        )

        self.assertEqual(expected_price, Solution.get_order_total_price(orderId))

    def createOrderWithDishes(self, orderId, dish1Id, dish2Id, dish3Id, dish1Amount, dish2Amount, dish3Amount) -> float:
        order = createOrder(order_id=orderId)
        dish1 = createDish(dish_id=dish1Id, price=1.414213)
        dish2 = createDish(dish_id=dish2Id, name="testDish2", price=2.71828)
        dish3 = createDish(dish_id=dish3Id, name="testDish3", price=3.141592)
        self.assertEqual(Solution.add_dish(dish1), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish2), ReturnValue.OK)
        self.assertEqual(Solution.add_dish(dish3), ReturnValue.OK)
        self.assertEqual(Solution.add_order(order), ReturnValue.OK)

        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish1.get_dish_id(), dish1Amount), ReturnValue.OK
        )
        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish2.get_dish_id(), dish2Amount), ReturnValue.OK
        )
        self.assertEqual(
            Solution.order_contains_dish(order.get_order_id(), dish3.get_dish_id(), dish3Amount), ReturnValue.OK
        )
        expected_price = (
                dish1.get_price() * dish1Amount + dish2.get_price() * dish2Amount + dish3.get_price() * dish3Amount
        )
        return expected_price

    def test_get_total_empty_order_price(self) -> None:
        order = createOrder()
        self.assertEqual(Solution.add_order(order), ReturnValue.OK)

        self.assertEqual(0, Solution.get_order_total_price(order.get_order_id()))

    def test_get_max_amount_of_money_cust_spent(self) -> None:
        customer = createCustomer()
        order1Id = 1
        order2Id = 2
        self.assertEqual(ReturnValue.OK, Solution.add_customer(customer))

        self.createOrderWithDishes(order1Id, 1, 2, 3, 23, 32, 45)
        expected_price = self.createOrderWithDishes(order2Id, 4, 5, 6, 432, 3543, 12)

        self.assertEqual(0, Solution.get_max_amount_of_money_cust_spent(customer.get_cust_id()))

        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(customer.get_cust_id(), order1Id))
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(customer.get_cust_id(), order2Id))

        self.assertEqual(expected_price, Solution.get_max_amount_of_money_cust_spent(customer.get_cust_id()))

    def test_get_most_expensive_anonymous_order(self) -> None:
        customer = createCustomer()
        order_with_cust = createOrder()
        anonymous_order_no_dish_low_id = createOrder(order_id=2)
        anonymous_order_cheap = createOrder(order_id=3)
        anonymous_order_expensive1 = createOrder(order_id=4)
        anonymous_order_expensive2 = createOrder(order_id=5)
        dish = createDish()

        self.assertEqual(ReturnValue.OK, Solution.add_customer(customer))
        self.assertEqual(ReturnValue.OK, Solution.add_order(order_with_cust))
        self.assertEqual(ReturnValue.OK, Solution.add_order(anonymous_order_cheap))
        self.assertEqual(ReturnValue.OK, Solution.add_order(anonymous_order_expensive1))
        self.assertEqual(ReturnValue.OK, Solution.add_order(anonymous_order_expensive2))
        self.assertEqual(ReturnValue.OK, Solution.add_order(anonymous_order_no_dish_low_id))
        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish))
        self.assertEqual(
            ReturnValue.OK, Solution.customer_placed_order(customer.get_cust_id(), order_with_cust.get_order_id())
        )

        assertOrdersEqual(
            self.assertEqual, anonymous_order_no_dish_low_id, Solution.get_most_expensive_anonymous_order()
        )

        self.assertEqual(
            ReturnValue.OK, Solution.order_contains_dish(order_with_cust.get_order_id(), dish.get_dish_id(), 34532)
        )
        self.assertEqual(
            ReturnValue.OK, Solution.order_contains_dish(anonymous_order_cheap.get_order_id(), dish.get_dish_id(), 1)
        )
        self.assertEqual(
            ReturnValue.OK,
            Solution.order_contains_dish(anonymous_order_expensive1.get_order_id(), dish.get_dish_id(), 50)
        )
        self.assertEqual(
            ReturnValue.OK,
            Solution.order_contains_dish(anonymous_order_expensive2.get_order_id(), dish.get_dish_id(), 50)
        )

        assertOrdersEqual(self.assertEqual, anonymous_order_expensive1, Solution.get_most_expensive_anonymous_order())

    def test_delete_order_with_dishes_and_customer_who_likes(self) -> None:
        customer = createCustomer()
        order = createOrder()
        dish = createDish()
        self.assertEqual(ReturnValue.OK, Solution.add_customer(customer))
        self.assertEqual(ReturnValue.OK, Solution.add_dish(dish))
        self.assertEqual(ReturnValue.OK, Solution.add_order(order))
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(order.get_order_id(), dish.get_dish_id(), 1))
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(customer.get_cust_id(), order.get_order_id()))
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(customer.get_cust_id(), dish.get_dish_id()))

        self.assertEqual(ReturnValue.OK, Solution.delete_order(order.get_order_id()))
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(customer.get_cust_id()))


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
