import unittest
import Solution as Solution
from Utility.ReturnValue import ReturnValue
from Tests.AbstractTest import AbstractTest
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish
from datetime import date, datetime
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
        c3 = Customer (1,'newname',"052222222","TelAviv")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_customer(c3), 'Customer already exists')
        c3 = Customer(-1, 'newname', "052222222", "TelAviv")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c3), 'negative id')
        c3 = Customer(-1, 'newname', "052222222", "TA")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c3), 'short address')
        c2 = Customer(2, 'name', None, "Haifa")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'invalid phone')
        c2 = Customer(2, 'name', "0502220000", None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'invalid address')
        c2 = Customer(None, 'name', "0502220000", "beersheva")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_customer(c2), 'invalid id')
        self.assertEqual(c1, Solution.get_customer(1), 'get customer check')
        self.assertEqual(BadCustomer(), Solution.get_customer(2), 'get customer check not exists')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(1), 'delete customer')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_customer(1), 'delete customer not exists')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_customer(-1), 'delete customer illegal id')

    def test_order(self)->None:
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        o1 = Order(1,datetime(2024,7,19,14,0,0))
        o2 = Order(-1,datetime.now())
        o3 = Order(2,datetime.now())
        o4 = Order(1,datetime(2022,12,24,14,30,0))
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'regular order')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_order(o2), 'negative order id')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'regular order')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_order(o4), 'already exists order id')
        self.assertEqual(o1, Solution.get_order(1), 'get order')
        self.assertEqual(BadOrder(), Solution.get_order(-1), 'get order negative input')
        self.assertEqual(BadOrder(), Solution.get_order(0), 'get order 0 input')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), ' customer placed order')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(1), 'order delete')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(1), 'delete order not exists')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(2), 'delete order')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.delete_order(-1), 'delete order bad params')
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(1), 'deleted from orders but not from all tables')

    def test_dish (self)->None:
        d1 = Dish(1,'salmon',89.89,True)
        d2 = Dish(1,'notSalmon',89.89,True)
        d4 = Dish(0,'salmon',89.89,True)
        d5 = Dish(2,'salmon',-89.89,True)
        d7 = Dish(1,'sa',89.89,True)
        d8 = Dish(1,'salmon',89.89,None)
        d3 = Dish(1,'salmon',None,True)
        d9 = Dish(1,None,150,True)
        d10 = Dish(1,None,150,False)
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'regular dish')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.add_dish(d2), 'ALREADY_EXISTS dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d4), 'bad param dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d5), 'bad param dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d7), 'bad param dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d8), 'bad param dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d9), 'bad param dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d10), 'bad param dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.add_dish(d3), 'bad param dish')
        self.assertEqual(d1, Solution.get_dish(1), 'get dish')
        self.assertEqual(BadDish(), Solution.get_dish(-1), 'get dish bad param')
        self.assertEqual(BadDish(), Solution.get_dish(2), 'get dish not exists')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1,50), 'update price')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.update_dish_price(1,-50), 'update price bad price')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_price(2,50), 'update price not exists')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_price(-2,50), 'update price illegal id')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_active_status(1,False), 'status change')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_price(1,500), 'update price dish not active')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_active_status(2,False), 'status change not exists')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.update_dish_active_status(-1,False), 'status change bad param')

    def test_customersPlacingOrders(self)->None :
        c2 = Customer (2,'newname',"052222222","TelAviv")
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        o1 = Order(1,datetime(2024,7,19,14,0,0))
        o4 = Order(2,datetime(2022,12,24,14,30,0))
        o3 = Order(3,datetime(2024,7,19,14,0,0))
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'regular customer')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'placing order')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(2,2), 'placing order')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.customer_placed_order(1,2), 'placing existing order by other customer')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.customer_placed_order(2,2), 'placing existing order by same customer')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_placed_order(2,4), 'regular customer')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_placed_order(5,5), 'regular customer')
        # looks wrong
        # self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_placed_order(-2,2), 'regular customer')
        self.assertEqual(c1, Solution.get_customer_that_placed_order(1), 'get customer by order id ')
        self.assertEqual(c2, Solution.get_customer_that_placed_order(2), 'get customer by order id ')
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(3), 'get customer by order id not placed')
        self.assertEqual(ReturnValue.OK, Solution.delete_customer(1), 'delete customer ')
        self.assertEqual(BadCustomer(), Solution.get_customer_that_placed_order(1), 'deleted from customer but not from all tables')
        #self.assertEqual(ReturnValue.ERROR, Solution.delete_customer(c1), 'ERROR Checking  ')

    def test_likes(self)->None :
        c2 = Customer (2,'newname',"052222222","TelAviv")
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        d1 = Dish(1,'salmon',89.89,True)
        d2 = Dish(2,'steak',130.89,True)
        d3 = Dish(3,'salad',23,True)
        d4 = Dish(4,'soup',59,True)

        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'regular customer')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(1,1), 'regular like')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(1,2), 'regular like')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(1,4), 'regular like')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.customer_likes_dish(1,1), 'already liked')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(10,1), 'bad param like')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(1,10), 'bad param like')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_likes_dish(-1,10), 'bad param like')
        self.assertEqual([d1,d2,d4], Solution.get_all_customer_likes(1), 'list likes')
        self.assertEqual([], Solution.get_all_customer_likes(2), 'list likes no likes by customer')
        self.assertEqual([], Solution.get_all_customer_likes(3), 'list likes customer not exist')
        self.assertEqual(ReturnValue.OK, Solution.customer_dislike_dish(1,4), 'dislike dish')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.customer_dislike_dish(1,3), 'DISLIKE not exists')
        self.assertEqual([d1,d2], Solution.get_all_customer_likes(1), 'list likes')

    def test_orderdishes(self)->None :
        d1 = Dish(1,'salmon',89.89,True)
        d2 = Dish(2,'steak',130.89,True)
        d3 = Dish(3,'salad',23,True)
        d4 = Dish(4,'soup',59,False)
        d5 = Dish(5,'GGGG',70,False)
        o1 = Order(1,datetime(2024,7,19,14,0,0))
        o2 = Order(2,datetime(2022,12,24,14,30,0))
        od1 = OrderDish(1,1,89.89)
        od2 = OrderDish(2,2,130.89)
        od3 = OrderDish(3,4,23)
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,1), 'contain dish')
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.order_contains_dish(1,2,-1), 'amount negative')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_contains_dish(1,4,1), 'dish inactive')
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.order_contains_dish(1,1,2), 'dish already in order')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_contains_dish(1,5,1), 'not exist dish')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_contains_dish(3,2,1), 'not exist order')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,2,2), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,3,4), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1,50), 'updtade price')
        self.assertEqual([od1,od2,od3], Solution.get_all_order_items(1), 'list of items')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(1,1), 'delete dish from order')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_does_not_contain_dish(1,5), 'delete dish from order not exist')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_does_not_contain_dish(7,5), 'delete dish from order bad param')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_does_not_contain_dish(1,7), 'delete dish from order bad param')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_does_not_contain_dish(-1,5), 'delete dish from order bad param')
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.order_does_not_contain_dish(1,-5), 'delete dish from order bad param')
        self.assertEqual([od2, od3], Solution.get_all_order_items(1), 'list of items')
        self.assertEqual([], Solution.get_all_order_items(2), 'list of items')
        self.assertEqual(ReturnValue.OK, Solution.delete_order(1), 'delete order')
        self.assertEqual([], Solution.get_all_order_items(1), 'list of items after deletion of order')

    def test_BasicAPI(self)->None :
        d1 = Dish(1, 'salmon', 89.89, True)
        d2 = Dish(2, 'steak', 130.89, True)
        d3 = Dish(3, 'salad', 23, True)
        d4 = Dish(4, 'soup', 59, True)
        d5 = Dish(5, 'GGGG', 70, True)
        o1 = Order(1, datetime(2024, 7, 19, 14, 0, 0))
        o2 = Order(2, datetime(2022, 12, 24, 14, 30, 0))
        o3 = Order(3, datetime(2024, 7, 19, 14, 0, 0)) # will be anonymous order
        o4 = Order(4, datetime(2024, 7, 19, 14, 0, 0)) # will be anonymous order
        c2 = Customer (2,'newname',"052222222","TelAviv")
        c1 = Customer(1, 'name', "0502220000", "Haifa")
        #self.assertEqual(False, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o1), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o2), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o3), 'regular order')
        self.assertEqual(ReturnValue.OK, Solution.add_order(o4), 'regular order')
       #self.assertEqual(False, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d1), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d2), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d3), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d4), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_dish(d5), 'regular dish')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c1), 'regular customer')
        self.assertEqual(ReturnValue.OK, Solution.add_customer(c2), 'regular customer')
        #self.assertEqual(False, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,2), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,2,2), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,3,2), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,4,2), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,5,2), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(2, 1, 1), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(2, 2, 1), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(2, 3, 1), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(2, 4, 1), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(2, 5, 1), 'contain dish')
        self.assertEqual(Solution.get_order_total_price(2)*2, Solution.get_order_total_price(1), 'get total price ')
        self.assertEqual(ReturnValue.OK, Solution.update_dish_price(1,50), 'updtade price')
        self.assertEqual(float(745.56), Solution.get_order_total_price(1), 'get total price after update prices')
        self.assertEqual(float(372.78), Solution.get_order_total_price(2), 'get total price after update prices')
        self.assertEqual(float(0), Solution.get_order_total_price(3), 'total for empty order')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,1), 'placing order')
        self.assertEqual(ReturnValue.OK, Solution.customer_placed_order(1,2), 'placing order')
        self.assertEqual(745.56, Solution.get_max_amount_of_money_cust_spent(1), 'maximum customer spent')
        self.assertEqual(float, type(Solution.get_max_amount_of_money_cust_spent(1)), 'type check')
        self.assertEqual(0, Solution.get_max_amount_of_money_cust_spent(2), 'maximum customer spent')
        self.assertEqual(float, type(Solution.get_max_amount_of_money_cust_spent(2)), 'type check')
        self.assertEqual(o3, Solution.get_most_expensive_anonymous_order(), 'anonymous check')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(4, 1, 1), 'contain dish')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(3, 1, 1), 'contain dish')
        self.assertEqual(o3, Solution.get_most_expensive_anonymous_order(), 'anonymous check')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(4, 2, 2), 'contain dish')
        self.assertEqual(o4, Solution.get_most_expensive_anonymous_order(), 'anonymous check')
        self.assertEqual(ReturnValue.OK, Solution.order_does_not_contain_dish(1,1), 'delete dish from order')
        self.assertEqual(float(565.78), Solution.get_order_total_price(1), 'get total price after update prices')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(1,1,2), 'contain dish')

        ## the following section will test is_most_liked_dish_equal_to_most_purchased
        #self.assertEqual(False, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(1,1), 'regular like')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(1,2), 'regular like')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(2,1), 'regular like')
        #self.assertEqual(True, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')
        self.assertEqual(ReturnValue.OK, Solution.customer_likes_dish(2,2), 'regular like')
        #self.assertEqual(True, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')
        self.assertEqual(ReturnValue.OK, Solution.order_contains_dish(3, 2, 20), 'contain dish')
        #self.assertEqual(False, Solution.is_most_liked_dish_equal_to_most_purchased(), ' liked most purchased')











# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)