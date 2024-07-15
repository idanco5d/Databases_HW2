from typing import List, Tuple
from psycopg2 import sql
from datetime import date, datetime
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Customer import Customer, BadCustomer
from Business.Order import Order, BadOrder
from Business.Dish import Dish, BadDish
from Business.OrderDish import OrderDish


# ---------------------------------- CRUD API: ----------------------------------
# Basic database functions


def create_tables() -> None:
    # check if can be changed
    connection = None
    try:
        connection = Connector.DBConnector()

        create_cust_table = ("create table customer "
                             "(cust_id integer check (cust_id > 0), "
                             "full_name text, "
                             "phone text, "
                             "address text check (length(address) > 2), "
                             "primary key (cust_id),"
                             "unique (cust_id));")
        create_order_table = ("create table order"
                              "(order_id integer check (order_id > 0),"
                              "date timestamp,"
                              "primary key (order_id),"
                              "unique (order_id));")
        create_dish_table = ("create table dish "
                             "(dish_id integer check (dish_id>0),"
                             "name text check (length(name) > 3),"
                             # to check precision
                             "price decimal check (price>0),"
                             "is_active boolean,"
                             "primary key (dish_id),"
                             "unique (dish_id));")
        queries = [create_cust_table, create_order_table, create_dish_table]
        for query in queries:
            connection.execute(query)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
    finally:
        connection.close()
    pass


def clear_tables() -> None:
    # TODO: implement
    pass


def drop_tables() -> None:
    connection = None
    try:
        connection = Connector.DBConnector()
        drop_customer = "drop table customer;"
        drop_order = "drop table order;"
        drop_dish = "drop table dish;"
        queries = [drop_customer, drop_order, drop_dish]
        for query in queries:
            connection.execute(query)
    except Exception as e:
        print(e)
    finally:
        connection.close()
    pass


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        if customer.get_cust_id() is None or customer.get_full_name() is None or customer.get_phone() is None or customer.get_address() is None:
            return ReturnValue.BAD_PARAMS
        query = ("insert into customer values (" + customer.get_cust_id().__str__() + ", '" + customer.get_full_name()
                 + "', '" + customer.get_phone() + "', '" + customer.get_address() + "');")
        connection.execute(query)

    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    finally:
        connection.close()
    return ReturnValue.OK

    pass


def get_customer(customer_id: int) -> Customer:
    connection = None
    customer = None
    try:
        connection = Connector.DBConnector()
        query = "select * from customer where cust_id = " + customer_id.__str__() + ";"
        _, result = connection.execute(query)
        if not result:
            customer = BadCustomer()
        else:
            db_result = result[0]
            customer = Customer(db_result['cust_id'], db_result['full_name'], db_result['phone'], db_result['address'])
    except Exception as e:
        print(e)
        return BadCustomer()
    finally:
        connection.close()
        return customer
    pass


def delete_customer(customer_id: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "DELETE FROM customer where cust_id= " + customer_id.__str__() + ";"
        connection.execute(query)

    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    #whatif customer doesn't exist
    finally:
        connection.close()
        return ReturnValue.OK
    pass


def add_order(order: Order) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = ("insert into order values (" + order.get_order_id().__str__() + ", '" + order.get_datetime().year.__str__() + "-" + order.get_datetime().month.__str__() + "-"+ order.get_datetime().day.__str__() + "');")
        connection.execute(query)

    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    finally:
        connection.close()
    return ReturnValue.OK
    pass


def get_order(order_id: int) -> Order:
    connection = None
    order = None
    try:
        connection = Connector.DBConnector()
        query = "select * from order where order_id = " + order_id.__str__() + ";"
        _, result = connection.execute(query)
        if not result:
            order = BadOrder()
        else:
            db_result = result[0]
            order = Order(db_result['order_id'], db_result['date'])
    except Exception as e:
        print(e)
        return BadOrder()
    finally:
        connection.close()
        return order
    pass


def delete_order(order_id: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "DELETE FROM order where order_id= " + order_id.__str__() + ";"
        connection.execute(query)

    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    # whatif order doesn't exist
    finally:
        connection.close()
        return ReturnValue.OK
        pass


def add_dish(dish: Dish) -> ReturnValue:
    # TODO: implement
    pass


def get_dish(dish_id: int) -> Dish:
    # TODO: implement
    pass


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    # TODO: implement
    pass


def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    # TODO: implement
    pass


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    # TODO: implement
    pass


def get_customer_that_placed_order(order_id: int) -> Customer:
    # TODO: implement
    pass


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    # TODO: implement
    pass


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass


def get_all_order_items(order_id: int) -> List[OrderDish]:
    # TODO: implement
    pass


def customer_likes_dish(cust_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass


def customer_dislike_dish(cust_id: int, dish_id: int) -> ReturnValue:
    # TODO: implement
    pass

def get_all_customer_likes(cust_id: int) -> List[Dish]:
    # TODO: implement
    pass
# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    # TODO: implement
    pass


def get_max_amount_of_money_cust_spent(cust_id: int) -> float:
    # TODO: implement
    pass


def get_most_expensive_anonymous_order() -> Order:
    # TODO: implement
    pass


def is_most_liked_dish_equal_to_most_purchased() -> bool:
    # TODO: implement
    pass


# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API


def get_customers_ordered_top_5_dishes() -> List[int]:
    # TODO: implement
    pass


def get_non_worth_price_increase() -> List[int]:
    # TODO: implement
    pass


def get_total_profit_per_month(year: int) -> List[Tuple[int, float]]:
    # TODO: implement
    pass


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    # TODO: implement
    pass
