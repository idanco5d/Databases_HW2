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
                             "unique (cust_id)); ")

        create_order_table = ("create table \"order\""
                              "(order_id integer check (order_id > 0),"
                              "date timestamp,"
                              "primary key (order_id),"
                              "unique (order_id)); ")

        create_dish_table = ("create table dish "
                             "(dish_id integer check (dish_id>0),"
                             "name text check (length(name) > 3),"
                             "price decimal check (price>0),"
                             "is_active boolean,"
                             "primary key (dish_id),"
                             "unique (dish_id)); ")

        create_customer_orders_table = ("create table customer_orders "
                                        "(cust_id integer,"
                                        "order_id integer,"
                                        "foreign key (cust_id) references customer(cust_id),"
                                        "foreign key (order_id) references \"order\"(order_id),"
                                        "primary key (order_id)); ")

        create_dishes_in_order_table = ("create table dishes_in_order "
                                        "(dish_id integer,"
                                        "order_id integer,"
                                        "foreign key (dish_id) references dish(dish_id),"
                                        "foreign key (order_id) references \"order\"(order_id),"
                                        "primary key (dish_id, order_id)); ")

        create_likes_table = ("create table likes "
                              "(cust_id integer,"
                              "dish_id integer,"
                              "foreign key (cust_id) references customer(cust_id),"
                              "foreign key (dish_id) references dish(dish_id),"
                              "primary key (dish_id, cust_id));")
        queries = [
            create_cust_table,
            create_order_table,
            create_dish_table,
            create_customer_orders_table,
            create_dishes_in_order_table,
            create_likes_table
        ]
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
        drop_likes = "drop table likes;"
        drop_dishes_in_order = "drop table dishes_in_order;"
        drop_customer_orders = "drop table customer_orders;"
        drop_customer = "drop table customer; "
        drop_order = "drop table \"order\"; "
        drop_dish = "drop table dish;"
        queries = [drop_customer_orders, drop_dishes_in_order, drop_likes, drop_customer, drop_order, drop_dish]
        for query in queries:
            connection.execute(query)
    except Exception as e:
        print(e)
    finally:
        connection.close()
    pass


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    if has_field_as_null(customer):
        return ReturnValue.BAD_PARAMS
    connection = None
    try:
        connection = Connector.DBConnector()
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
        customer = BadCustomer()
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
    # whatif customer doesn't exist
    finally:
        connection.close()
        return ReturnValue.OK
    pass


def add_order(order: Order) -> ReturnValue:
    if has_field_as_null(order):
        return ReturnValue.BAD_PARAMS
    connection = None
    try:
        connection = Connector.DBConnector()
        query = (
                    "insert into \"order\" values (" + order.get_order_id().__str__() + ", '" + order.get_datetime().year.__str__() + "-" + order.get_datetime().month.__str__() + "-" + order.get_datetime().day.__str__() + "');")
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
        query = "select * from \"order\" where order_id = " + order_id.__str__() + ";"
        _, result = connection.execute(query)
        if not result:
            order = BadOrder()
        else:
            db_result = result[0]
            order = Order(db_result['order_id'], db_result['date'])
    except Exception as e:
        print(e)
        order = BadOrder()
    finally:
        connection.close()
        return order
    pass


def delete_order(order_id: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "DELETE FROM \"order\" where order_id= " + order_id.__str__() + ";"
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
    if has_field_as_null(dish):
        return ReturnValue.BAD_PARAMS
    connection = None
    try:
        connection = Connector.DBConnector()
        query = (
                "insert into dish values (" + dish.get_dish_id().__str__() + ", '" + dish.get_name() + "', " + dish.get_price().__str__() + ", " + dish.get_is_active().__str__() + ");"
        )
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


def get_dish(dish_id: int) -> Dish:
    connection = None
    dish = None
    try:
        connection = Connector.DBConnector()
        query = "select * from dish where dish_id = " + dish_id.__str__() + ";"
        _, result = connection.execute(query)
        if not result:
            dish = BadDish()
        else:
            db_result = result[0]
            dish = Dish(db_result['dish_id'], db_result['name'], db_result['price'], db_result['is_active'])
    except Exception as e:
        print(e)
        dish = BadDish()
    finally:
        connection.close()
        return dish
    pass


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "update dish set price = " + price.__str__() + " where dish_id = " + dish_id.__str__() + ";"
        connection.execute(query)
    except DatabaseException.CHECK_VIOLATION as e:
        connection.close()
        return ReturnValue.BAD_PARAMS
    return ReturnValue.OK
    pass


def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "update dish set is_active = " + is_active.__str__() + " where dish_id = " + dish_id.__str__() + ";"
        connection.execute(query)
    except DatabaseException.CHECK_VIOLATION as e:
        connection.close()
        return ReturnValue.BAD_PARAMS
    return ReturnValue.OK


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    connection = None

    try:
        connection = Connector.DBConnector()
        query1 = ("insert into customer_orders values (" + customer_id.__str__() + ", '" + order_id.__str__() + "');")
        query2 = ("update \"order\" set date=current_date where order = (" + order_id.__str__() + ");")
        queries = [query1, query2]
        for query in queries:
            connection.execute(query)

    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.NOT_EXISTS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.BAD_PARAMS
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.ERROR
    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    finally:
        connection.close()
    pass


def get_customer_that_placed_order(order_id: int) -> Customer:
    connection = None
    customer = None
    try:
        connection = Connector.DBConnector()
        query = "select cust_id from customer_orders where order_id = " + order_id.__str__() + ";"
        _, result = connection.execute(query)
        if not result:
            customer = BadCustomer()
        else:
            customer = get_customer(result)
    except Exception as e:
        print(e)
        return BadCustomer()
    finally:
        connection.close()
        return customer
    pass


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query1 = ("insert into dishes_in_order values (" + order_id.__str__() + ", '" + dish_id.__str__() + "');")
        # query2 = ("update price set date=current_date where order = (" + order_id.__str__() + ");")
        # add price in dishes_in_order
        queries = [query1]
        for query in queries:
            connection.execute(query)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.ERROR
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        return ReturnValue.ERROR
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        return ReturnValue.ERROR
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        return ReturnValue.ERROR
    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    finally:
        connection.close()
        return ReturnValue.OK
    pass


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "DELETE FROM dishes_in_order where order_id= " + order_id.__str__() + " AND dish_id= " + dish_id.__str__() + ";"

    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        return ReturnValue.NOT_EXISTS
    except Exception as e:
        print(e)
        return ReturnValue.ERROR
    finally:
        connection.close()
        return ReturnValue.OK
        pass


def get_all_order_items(order_id: int) -> List[OrderDish]:
    try:
        connection = Connector.DBConnector()
        query = ("select d.dish_id, d.price, count(*) amount "
                 "from \"order\" o "
                 "join dishes_in_order dio on dio.order_id = o.order_id "
                 "join dish d on d.dish_id = dio.dish_id "
                 "where o.order_id = " + order_id.__str__()
                 + " group by d.dish_id, d.price "
                   "order by d.dish_id;")
        _, result = connection.execute(query)
        orders_dishes = [
            OrderDish(order_dish['dish_id'], order_dish['amount'], order_dish['price']) for order_dish in result
        ]
    except DatabaseException.ConnectionInvalid:
        return []
    connection.close()
    return orders_dishes
    pass


def customer_likes_dish(cust_id: int, dish_id: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = ("insert into likes values(" + cust_id.__str__() + ", '" + dish_id.__str__() + "');")
        connection.execute(query)
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        connection.close()
        return ReturnValue.NOT_EXISTS
    return ReturnValue.OK
    pass


def customer_dislike_dish(cust_id: int, dish_id: int) -> ReturnValue:
    try:
        connection = Connector.DBConnector()
        query = ("delete from likes "
                 "where cust_id = " + cust_id.__str__() +
                 " and dish_id = " + dish_id.__str__() + ";")
        rows_affected, _ = connection.execute(query)
        if rows_affected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    return ReturnValue.OK
    pass


def get_all_customer_likes(cust_id: int) -> List[Dish]:
    try:
        connection = Connector.DBConnector()
        query = ("select d.dish_id, d.name, d.price, d.is_active "
                 "from dish d "
                 "join likes l on l.dish_id = d.dish_id "
                 "where l.cust_id = " + cust_id.__str__() + ";")
        _, result = connection.execute(query)
        dishes = [Dish(dish['dish_id'], dish['name'], dish['price'], dish['is_active']) for dish in result]
    except DatabaseException.ConnectionInvalid:
        return []
    return dishes


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


def has_field_as_null(instance):
    return any(value is None for value in vars(instance).values())
