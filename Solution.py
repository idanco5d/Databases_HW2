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
    connection = Connector.DBConnector()

    create_cust_table = ("create table customer "
                         "(cust_id integer not null check (cust_id > 0), "
                         "full_name text not null, "
                         "phone text not null, "
                         "address text not null check (length(address) > 2), "
                         "primary key (cust_id)"
                         "); ")

    create_order_table = ("create table \"order\""
                          "(order_id integer not null check (order_id > 0),"
                          "date timestamp not null,"
                          "primary key (order_id)"
                          "); ")

    create_dish_table = ("create table dish "
                         "(dish_id integer not null check (dish_id>0),"
                         "name text not null check (length(name) > 2),"
                         "price decimal not null check (price>0),"
                         "is_active boolean,"
                         "primary key (dish_id)"
                         "); ")

    create_customer_orders_table = ("create table customer_orders "
                                    "(cust_id integer,"
                                    "order_id integer,"
                                    "foreign key (cust_id) references customer(cust_id),"
                                    "foreign key (order_id) references \"order\"(order_id),"
                                    "primary key (order_id)); ")

    create_dishes_in_order_table = ("create table dishes_in_order "
                                    "(dish_id integer,"
                                    "order_id integer,"
                                    "amount integer not null check (amount>0),"
                                    "dish_price decimal not null,"
                                    "foreign key (dish_id) references dish(dish_id),"
                                    "foreign key (order_id) references \"order\"(order_id),"
                                    "primary key (dish_id, order_id)); ")

    create_likes_table = ("create table likes "
                          "(cust_id integer,"
                          "dish_id integer,"
                          "foreign key (cust_id) references customer(cust_id),"
                          "foreign key (dish_id) references dish(dish_id),"
                          "primary key (dish_id, cust_id));")

    create_view_orders_total_price = ("create view orders_total_price as "
                                      "(select sum(amount * dish_price) as order_price, dio.order_id "
                                      "from dishes_in_order dio "
                                      "group by dio.order_id);")
    query = (create_cust_table +
             create_order_table +
             create_dish_table +
             create_customer_orders_table +
             create_dishes_in_order_table +
             create_likes_table +
             create_view_orders_total_price)
    connection.execute(query)
    connection.close()


def clear_tables() -> None:
    connection = Connector.DBConnector()
    query = ("delete from likes; "
             "delete from dishes_in_order; "
             "delete from customer_orders; "
             "delete from customer; "
             "delete from \"order\"; "
             "delete from dish;")
    connection.execute(query)
    connection.close()


def drop_tables() -> None:
    connection = Connector.DBConnector()
    drop_orders_view = "drop view orders_total_price; "
    drop_likes = "drop table likes; "
    drop_dishes_in_order = "drop table dishes_in_order; "
    drop_customer_orders = "drop table customer_orders; "
    drop_customer = "drop table customer; "
    drop_order = "drop table \"order\"; "
    drop_dish = "drop table dish;"
    query = (drop_orders_view
             + drop_customer_orders
             + drop_dishes_in_order
             + drop_likes
             + drop_customer
             + drop_order
             + drop_dish)

    connection.execute(query)
    connection.close()


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
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.ConnectionInvalid:
        connection.close()
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def get_customer(customer_id: int) -> Customer:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "select * from customer where cust_id = " + customer_id.__str__() + ";"
        _, result = connection.execute(query)
        if result.size() == 0:
            customer = BadCustomer()
        else:
            db_result = result[0]
            customer = Customer(db_result['cust_id'], db_result['full_name'], db_result['phone'], db_result['address'])
    except DatabaseException.ConnectionInvalid:
        customer = BadCustomer()
    connection.close()
    return customer


def delete_customer(customer_id: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = ("delete from customer_orders where cust_id = " + customer_id.__str__() + "; "
                 "delete from likes where cust_id = " + customer_id.__str__() + "; "                          
                 "DELETE FROM customer where cust_id= ") + customer_id.__str__() + ";"
        rows_effected, _ = connection.execute(query)
        if rows_effected == 0:
            connection.close()
            return ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid:
        connection.close()
        return ReturnValue.ERROR
    return ReturnValue.OK


def add_order(order: Order) -> ReturnValue:
    if has_field_as_null(order):
        return ReturnValue.BAD_PARAMS
    connection = None
    try:
        connection = Connector.DBConnector()
        orderDate = order.get_datetime()
        query = (
                    "insert into \"order\" "
                    "values ("
                    + order.get_order_id().__str__()
                    + ", '" + orderDate.year.__str__()
                    + "-" + orderDate.month.__str__()
                    + "-" + orderDate.day.__str__()
                    + " " + orderDate.hour.__str__()
                    + ":" + orderDate.minute.__str__()
                    + ":" + orderDate.second.__str__()
                    + "');")
        connection.execute(query)

    except DatabaseException.NOT_NULL_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def get_order(order_id: int) -> Order:
    try:
        connection = Connector.DBConnector()
        query = "select * from \"order\" where order_id = " + order_id.__str__() + ";"
        _, result = connection.execute(query)
        if result.size() == 0:
            order = BadOrder()
        else:
            db_result = result[0]
            order = Order(db_result['order_id'], db_result['date'])
    except DatabaseException.ConnectionInvalid:
        return BadOrder()
    connection.close()
    return order


def delete_order(order_id: int) -> ReturnValue:
    try:
        connection = Connector.DBConnector()
        query = ("delete from customer_orders where order_id = " + order_id.__str__() + ";"
                 " delete from dishes_in_order where order_id = " + order_id.__str__() + ";"
                 " DELETE FROM \"order\" where order_id= " + order_id.__str__() + ";")
        rows_effected, _ = connection.execute(query)
        if rows_effected == 0:
            connection.close()
            return ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


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
    except DatabaseException.CHECK_VIOLATION as e:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def get_dish(dish_id: int) -> Dish:
    try:
        connection = Connector.DBConnector()
        query = "select * from dish where dish_id = " + dish_id.__str__() + ";"
        _, result = connection.execute(query)
        if result.size() == 0:
            dish = BadDish()
        else:
            db_result = result[0]
            dish = Dish(db_result['dish_id'], db_result['name'], db_result['price'], db_result['is_active'])
    except DatabaseException.ConnectionInvalid:
        return BadDish()
    connection.close()
    return dish


def update_dish_price(dish_id: int, price: float) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = (("update dish "
                 "set price = ") + price.__str__()
                 + " where dish_id = " + dish_id.__str__() + " and is_active = true;")
        rows_affected, _ = connection.execute(query)
        if rows_affected == 0:
            connection.close()
            return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def update_dish_active_status(dish_id: int, is_active: bool) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = "update dish set is_active = " + is_active.__str__() + " where dish_id = " + dish_id.__str__() + ";"
        rows_affected, _ = connection.execute(query)
        if rows_affected == 0:
            connection.close()
            return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION as e:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    connection = None

    try:
        connection = Connector.DBConnector()
        query = ("insert into customer_orders values (" + customer_id.__str__() + ", '" + order_id.__str__() + "');")
        connection.execute(query)

    except DatabaseException.FOREIGN_KEY_VIOLATION:
        connection.close()
        return ReturnValue.NOT_EXISTS
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def get_customer_that_placed_order(order_id: int) -> Customer:
    try:
        connection = Connector.DBConnector()
        query = "select c.* from customer_orders co " \
                "join customer c on c.cust_id = co.cust_id " \
                "where order_id = " + order_id.__str__() + ";"
        _, result = connection.execute(query)
        if result.size() == 0:
            customer = BadCustomer()
        else:
            customer = Customer(result["cust_id"][0], result["full_name"][0], result["phone"][0], result["address"][0])
    except DatabaseException.ConnectionInvalid:
        return BadCustomer()
    connection.close()
    return customer


def order_contains_dish(order_id: int, dish_id: int, amount: int) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = ("insert into dishes_in_order "
                 "values ("
                 + dish_id.__str__() + ", "
                 + order_id.__str__() + ", "
                 + amount.__str__()
                 + ", (select price "
                   "from dish "
                   "where dish_id = " + dish_id.__str__()
                 + " and is_active = true"
                   "));")
        connection.execute(query)
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        connection.close()
        return ReturnValue.NOT_EXISTS
    except DatabaseException.NOT_NULL_VIOLATION:
        connection.close()
        return ReturnValue.NOT_EXISTS
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def order_does_not_contain_dish(order_id: int, dish_id: int) -> ReturnValue:
    try:
        connection = Connector.DBConnector()
        query = "DELETE FROM dishes_in_order where order_id= " + order_id.__str__() + " AND dish_id= " + dish_id.__str__() + ";"
        row_effected, _ = connection.execute(query)
        if row_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def get_all_order_items(order_id: int) -> List[OrderDish]:
    try:
        connection = Connector.DBConnector()
        query = ("select dish_id, dish_price, amount "
                 "from dishes_in_order "
                 "where order_id = " + order_id.__str__() +
                 " order by dish_id;")
        _, result = connection.execute(query)
        orders_dishes = [
            OrderDish(order_dish['dish_id'], order_dish['amount'], order_dish['dish_price']) for order_dish in result
        ]
    except DatabaseException.ConnectionInvalid:
        return []
    connection.close()
    return orders_dishes


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
    try:
        connection = Connector.DBConnector()
        query = "select order_price from orders_total_price where order_id = " + order_id.__str__() + ";"
        _, result = connection.execute(query)
    except DatabaseException.ConnectionInvalid:
        return -1
    if result.size() == 0:
        return float(0)
    return float(result[0]['order_price'])


def get_max_amount_of_money_cust_spent(cust_id: int) -> float:
    try:
        connection = Connector.DBConnector()
        query = ("select max(order_price) max_price "
                 "from orders_total_price otp "
                 "join customer_orders co on co.order_id = otp.order_id "
                 "where co.cust_id = " + cust_id.__str__() + ";")
        _, result = connection.execute(query)
    except DatabaseException.ConnectionInvalid:
        return float(0)
    price = result[0]['max_price']
    return float(0 if price is None else price)


def get_most_expensive_anonymous_order() -> Order:
    try:
        connection = Connector.DBConnector()
        query = ("select coalesce(max(otp.order_price),0) max_price, o.order_id, o.date "
                 "from \"order\" o "
                 "left join orders_total_price otp on o.order_id = otp.order_id "
                 "where not exists (select 1 from customer_orders co where co.order_id = o.order_id) "
                 "group by o.order_id, o.date "
                 "order by max_price desc limit 1")
        _, result = connection.execute(query)
        connection.close()
        return Order(result['order_id'][0], result['date'][0])
    except DatabaseException.ConnectionInvalid:
        return BadOrder()


def is_most_liked_dish_equal_to_most_purchased() -> bool:
    query = ""
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
