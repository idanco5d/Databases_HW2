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
    query = sql.SQL("""create table customer (
                        cust_id integer not null check (cust_id > 0), 
                        full_name text not null, 
                        phone text not null, 
                        address text not null check (length(address) > 2), 
                        primary key (cust_id)
                        ); 
                        create table "order" (
                        order_id integer not null check (order_id > 0),
                        date timestamp(0) not null,
                        primary key (order_id)
                        );
                        create table dish (
                        dish_id integer not null check (dish_id>0),
                        name text not null check (length(name) > 2),
                        price decimal not null check (price>0),
                        is_active boolean not null,
                        primary key (dish_id)
                        );
                        create table customer_orders (
                        cust_id integer,
                        order_id integer,
                        foreign key (cust_id) references customer(cust_id) on delete cascade,
                        foreign key (order_id) references "order"(order_id) on delete cascade,
                        primary key (order_id)
                        );
                        create table dishes_in_order (
                        dish_id integer,
                        order_id integer,
                        amount integer not null check (amount>0),
                        dish_price decimal not null,
                        foreign key (dish_id) references dish(dish_id) on delete cascade,
                        foreign key (order_id) references "order"(order_id) on delete cascade,
                        primary key (dish_id, order_id)
                        );
                        create table likes (
                        cust_id integer,
                        dish_id integer,
                        foreign key (cust_id) references customer(cust_id) on delete cascade,
                        foreign key (dish_id) references dish(dish_id) on delete cascade,
                        primary key (dish_id, cust_id)
                        );
                        create view dish_profit_in_order as
                        select amount * dish_price dish_profit, dish_id, order_id, dish_price
                        from dishes_in_order;
                        create view orders_total_price as 
                        select sum(dish_profit) order_price, order_id 
                        from dish_profit_in_order
                        group by order_id;
                         """)

    connection.execute(query)
    connection.close()


def clear_tables() -> None:
    connection = Connector.DBConnector()
    query = sql.SQL("""delete from likes; 
             delete from dishes_in_order; 
             delete from customer_orders; 
             delete from customer; 
             delete from "order"; 
             delete from dish;""")
    connection.execute(query)
    connection.close()


def drop_tables() -> None:
    connection = Connector.DBConnector()
    query = sql.SQL("""
                        drop view orders_total_price;
                        drop view dish_profit_in_order;
                        drop table likes;
                        drop table dishes_in_order;
                        drop table customer_orders;
                        drop table customer;
                        drop table "order";
                        drop table dish;
                        """)
    connection.execute(query)
    connection.close()


# CRUD API

def add_customer(customer: Customer) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = sql.SQL(
            """insert into customer values({cust_id}, {cust_fullname}, {cust_phone}, {cust_adress});"""
        ).format(
            cust_id=sql.Literal(customer.get_cust_id()),
            cust_fullname=sql.Literal(customer.get_full_name()),
            cust_phone=sql.Literal(customer.get_phone()),
            cust_adress=sql.Literal(customer.get_address())
        )
        connection.execute(query)
        connection.close()
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.ConnectionInvalid:
        connection.close()
        return ReturnValue.ERROR
    return ReturnValue.OK


def get_customer(customer_id: int) -> Customer:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = sql.SQL(
            """select * from customer where cust_id = {cust};"""
        ).format(cust=sql.Literal(customer_id))

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
        query = sql.SQL("""
                        delete from customer where cust_id= {cust};
                        """).format(cust=sql.Literal(customer_id))

        rows_effected, _ = connection.execute(query)
        connection.close()

        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid:
        connection.close()
        return ReturnValue.ERROR
    return ReturnValue.OK


def add_order(order: Order) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = sql.SQL(
            """insert into "order" values({orderID}, {date});"""
        ).format(
            orderID=sql.Literal(order.get_order_id()),
            date=sql.Literal(order.get_datetime())
        )
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
        query = sql.SQL("""
                        select * from "order" where order_id = {orderID};
                        """).format(orderID=sql.Literal(order_id))
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
        query = sql.SQL("""
                        DELETE FROM "order" where order_id = {order};
                        """).format(order=sql.Literal(order_id))

        rows_effected, _ = connection.execute(query)
        connection.close()
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    return ReturnValue.OK


def add_dish(dish: Dish) -> ReturnValue:
    connection = None
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                        insert into dish values({dishid}, {name}, {price}, {active});
                        """).format(dishid=sql.Literal(dish.get_dish_id()),
                                    name=sql.Literal(dish.get_name()),
                                    price=sql.Literal(dish.get_price()),
                                    active=sql.Literal(dish.get_is_active()))

        connection.execute(query)
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.NOT_NULL_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        connection.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    connection.close()
    return ReturnValue.OK


def get_dish(dish_id: int) -> Dish:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                          select * from dish where dish_id = {dish_id};
                          """).format(dish_id=sql.Literal(dish_id))
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
        query = sql.SQL("""
                        update dish 
                        set price= {price}
                        where dish_id = {dish} and is_active = true;
                        """).format(price=sql.Literal(price),
                                    dish=sql.Literal(dish_id))
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
        query = sql.SQL("""
            update dish set is_active= {active} where dish_id = {dish};
        """).format(active=sql.Literal(is_active),
                    dish=sql.Literal(dish_id))

        rows_affected, _ = connection.execute(query)
        connection.close()
        if rows_affected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.CHECK_VIOLATION:
        connection.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    return ReturnValue.OK


def customer_placed_order(customer_id: int, order_id: int) -> ReturnValue:
    connection = None

    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                        insert into customer_orders values({cust_id}, {ord_id});
                        """).format(cust_id=sql.Literal(customer_id),
                                    ord_id=sql.Literal(order_id))
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
        query = sql.SQL("""
                         select c.* from customer_orders co 
                         join customer c on c.cust_id = co.cust_id
                         where order_id= {order};
                          """).format(order=sql.Literal(order_id))

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
        query = sql.SQL("""
                        insert into dishes_in_order values({dishid}, {ord_id}, {amount},
                        (select price
                        from dish
                        where dish_id={dishid} and is_active = true));
                        """).format(dishid=sql.Literal(dish_id),
                                    ord_id=sql.Literal(order_id),
                                    amount=sql.Literal(amount))

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
        query = sql.SQL("""
                        delete from dishes_in_order where order_id = {order} and dish_id= {dishid};
                        """).format(order=sql.Literal(order_id),
                                    dishid=sql.Literal(dish_id))
        row_effected, _ = connection.execute(query)
        connection.close()
        if row_effected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    return ReturnValue.OK


def get_all_order_items(order_id: int) -> List[OrderDish]:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                         select dish_id, dish_price, amount
                         from dishes_in_order 
                         where order_id= {order}
                         order by dish_id;
                          """).format(order=sql.Literal(order_id))

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
        query = sql.SQL("""
                        insert into likes values({cust_id}, {dish_id});
                        """).format(cust_id=sql.Literal(cust_id),
                                    dish_id=sql.Literal(dish_id))
        connection.execute(query)
        connection.close()
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
        query = sql.SQL("""
                        delete from likes 
                        where cust_id = {cust} and dish_id= {dishid};
                        """).format(cust=sql.Literal(cust_id),
                                    dishid=sql.Literal(dish_id))

        rows_affected, _ = connection.execute(query)
        connection.close()
        if rows_affected == 0:
            return ReturnValue.NOT_EXISTS
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR
    return ReturnValue.OK


def get_all_customer_likes(cust_id: int) -> List[Dish]:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                         select d.dish_id, d.name, d.price, d.is_active
                         from dish d 
                         join likes l on l.dish_id = d.dish_id
                         where l.cust_id= {cust};
                          """).format(cust=sql.Literal(cust_id))
        _, result = connection.execute(query)
        dishes = [Dish(dish['dish_id'], dish['name'], dish['price'], dish['is_active']) for dish in result]
        connection.close()
    except DatabaseException.ConnectionInvalid:
        return []
    return dishes


# ---------------------------------- BASIC API: ----------------------------------

# Basic API


def get_order_total_price(order_id: int) -> float:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                         select order_price
                         from orders_total_price 
                         where order_id= {ord_id};
                          """).format(ord_id=sql.Literal(order_id))
        _, result = connection.execute(query)
        connection.close()
    except DatabaseException.ConnectionInvalid:
        return -1
    if result.size() == 0:
        return float(0)
    return float(result[0]['order_price'])


def get_max_amount_of_money_cust_spent(cust_id: int) -> float:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                         select max(order_price) max_price
                         from orders_total_price otp 
                         join customer_orders co on co.order_id = otp.order_id
                         where co.cust_id= {cust};
                          """).format(cust=sql.Literal(cust_id))
        _, result = connection.execute(query)
        connection.close()
    except DatabaseException.ConnectionInvalid:
        return float(0)
    price = result[0]['max_price']
    return float(0 if price is None else price)


def get_most_expensive_anonymous_order() -> Order:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                         select coalesce(max(otp.order_price),0) max_price, o.order_id, o.date
                         from "order" o 
                         left join orders_total_price otp on o.order_id = otp.order_id
                         where not exists (select 1 from customer_orders co where co.order_id = o.order_id)
                         group by o.order_id, o.date
                         order by max_price desc limit 1;
                          """)

        _, result = connection.execute(query)
        connection.close()
        return Order(result['order_id'][0], result['date'][0])
    except DatabaseException.ConnectionInvalid:
        return BadOrder()


def is_most_liked_dish_equal_to_most_purchased() -> bool:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
                select dish_like.dish_id = dish_purch.dish_id bool_dish 
                from (select dish_id,count (*) 
                      from likes 
                      group by dish_id 
                      order by count (*) desc ,dish_id limit 1 ) dish_like,
                      (select dish_id, sum(amount) 
                       from dishes_in_order 
                       group by dish_id 
                       order by sum(amount) desc ,dish_id limit 1 ) dish_purch;
                    """)
        _, result = connection.execute(query)
        connection.close()
        return result["bool_dish"][0] if result.size() > 0 else False
    except DatabaseException.ConnectionInvalid:
        return False


# ---------------------------------- ADVANCED API: ----------------------------------

# Advanced API


def get_customers_ordered_top_5_dishes() -> List[int]:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
            select distinct cust_id
            from customer_orders co 
            join (
                select count(*), order_id
                from dishes_in_order dio
                where dish_id in
                (
                    select dish_id from (
                    select d.dish_id, count(l.dish_id) 
                    from dish d
                    left join likes l on l.dish_id = d.dish_id
                    group by d.dish_id
                    order by count(l.dish_id) desc, d.dish_id limit 5
                    )
                )
                group by order_id
                having count(*) = 5
            ) orders
            on orders.order_id = co.order_id
            order by cust_id
        """)
        _, result = connection.execute(query)
        connection.close()
        return result['cust_id']
    except DatabaseException.ConnectionInvalid:
        return []


def get_non_worth_price_increase() -> List[int]:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
        with avg_dish_price as (
        select avg(dish_profit) avg_profit, dish_price, dish_id
        from dish_profit_in_order
        group by dish_price, dish_id
        )
        select distinct d.dish_id
        from dish d
        join avg_dish_price curr_avg 
        on curr_avg.dish_id = d.dish_id and curr_avg.dish_price = d.price
        join avg_dish_price former_avg
        on former_avg.dish_id = d.dish_id and former_avg.dish_price <> d.price
        where d.is_active = true
        and curr_avg.avg_profit < former_avg.avg_profit
        order by d.dish_id
        """)
        _, result = connection.execute(query)
        connection.close()
        return result['dish_id']
    except DatabaseException.ConnectionInvalid:
        return []


def get_total_profit_per_month(year: int) -> List[Tuple[int, float]]:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
        select months.month, coalesce(sum(dpio.dish_profit), 0) price
        from (select generate_series(1, 12) "month") months
        left join "order" o 
        on extract(month from o.date) = months.month and extract(year from o.date) = {input_year}
        left join dish_profit_in_order dpio 
        on dpio.order_id = o.order_id
        group by months.month
        order by months.month desc
        """).format(input_year=sql.Literal(year))
        _, result = connection.execute(query)
        connection.close()
        return [(int(row['month']), float(row['price'])) for row in result]
    except DatabaseException.ConnectionInvalid:
        return []


def get_potential_dish_recommendations(cust_id: int) -> List[int]:
    try:
        connection = Connector.DBConnector()
        query = sql.SQL("""
            select distinct l.dish_id dish_recommendations
            from likes l
            where l.cust_id in (
                select l2.cust_id
                from likes l1
                join likes l2 on l1.dish_id = l2.dish_id
                where l1.cust_id = {cust_id}
                and l1.cust_id <> l2.cust_id
                group by l2.cust_id
                having count(*) > 2
            )
            and not exists (
                select 1
                from likes l3
                where l3.dish_id = l.dish_id
                and l3.cust_id = {cust_id}
            )
            order by l.dish_id
        """).format(cust_id=sql.Literal(cust_id))
        _, result = connection.execute(query)
        connection.close()
        return result['dish_recommendations']
    except DatabaseException.ConnectionInvalid:
        return []
