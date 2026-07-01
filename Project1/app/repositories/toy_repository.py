"""
The toy repository methods handles all interactions with the database directly
"""
from app.models.toy import Toy
import app.utils.db_connection_util as conn

def record_to_toy(record) -> Toy:
    """
    Turns an individual record from the database into a toy object
    :param record: An individual toy record from the database
    :return: A toy object based on the given record
    """
    return Toy(toy_id = record[0],
               name = record[1],
               manufacturer = record[2],
               weight = record[3],
               price = record[4],
               units_sold = record[5])


def open_conn_and_cursor():

    """
    Instantiates a new instance of a connection and its cursor
    :return: The new connection and its associated cursor
    """
    connection = conn.get_connection()
    cursor = connection.cursor()
    return connection, cursor


def close_conn_and_cursor(connection, cursor):
    """
    Closes the current cursor and connection
    :param connection: The current connection
    :param cursor: The current cursor
    :return: None
    """
    cursor.close()
    connection.close()


def add_toy(toy: Toy) :
    """
    Adds the given toy into the database
    :param toy: The toy that is going to be added into the database
    :return: None
    """

    connection, cursor = open_conn_and_cursor()
    cursor.execute("""
                   INSERT INTO toys (name, manufacturer, weight, price, units_sold) VALUES
                       (%s, %s, %s, %s, %s)
                   """,(toy.name,toy.manufacturer, toy.weight, toy.price,toy.units_sold))

    connection.commit()
    close_conn_and_cursor(connection, cursor)


def get_toy_by_id(toy_id:int) -> Toy | None:
    """
    Gets the toy in the database based on the given ID
    :param toy_id: The ID of the toy in the database
    :return: The toy in the database that matches the given ID.
    If there is no toy matching the given ID, the method returns None
    """
    connection, cursor = open_conn_and_cursor()

    cursor.execute("SELECT * FROM toys WHERE toy_id = %s", (toy_id,))
    record = cursor.fetchone() # Only getting a single record

    close_conn_and_cursor(connection, cursor)

    if record is None:
        return None

    return record_to_toy(record)


def get_all_toys() -> list[Toy]:
    """
    Gets all the toys that are listed in the database
    :return: All the toys in the database
    """
    connection, cursor = open_conn_and_cursor()

    cursor.execute("SELECT * FROM toys")
    results = cursor.fetchall() # Gets the results of the SELECT

    close_conn_and_cursor(connection, cursor)
    return [record_to_toy(record) for record in results]


def get_all_toys_by_manufacturer(manufacturer: str) -> list[Toy]:
    """
    Gets all the toys listed in the database that have the given manufacturer
    :param manufacturer: The manufacturer of toys in the database
    :return: All the toys in the database that have the given manufacturer
    """
    connection, cursor = open_conn_and_cursor()

    cursor.execute("SELECT * FROM toys WHERE manufacturer = %s", (manufacturer,))
    results = cursor.fetchall() # Gets the results of the SELECT

    close_conn_and_cursor(connection, cursor)
    return [record_to_toy(record) for record in results]


def get_all_toys_by_price_cap(price_cap: float) -> list[Toy]:
    """
    Gets all the toys from the database that are less than or equal to the given price cap
    :param price_cap: The cap that all toys are less than or equal to in the database
    :return: All the toys from the database that are less than or equal to the given price cap
    """
    connection, cursor = open_conn_and_cursor()

    cursor.execute("SELECT * FROM toys WHERE price <= %s", (price_cap,))
    results = cursor.fetchall() # Gets the results of the SELECT

    close_conn_and_cursor(connection, cursor)
    return [record_to_toy(record) for record in results]


def update_toy_name_by_id(toy_id: int, new_name: str) -> Toy | None:
    """
    Updates the toy's name in the database based on the given ID
    :param toy_id: The ID of the toy in the database
    :param new_name: The new name of the toy in the database
    :return: The updated toy in the database that matches the given ID.
    If there is no toy matching the given ID, the method returns None
    """

    toy_to_update = get_toy_by_id(toy_id)
    if not toy_to_update:
        return None

    connection, cursor = open_conn_and_cursor()
    cursor.execute(
        "UPDATE toys SET name = %s WHERE toy_id = %s",
        (new_name, toy_id)
    )

    connection.commit()
    close_conn_and_cursor(connection, cursor)

    updated_toy = get_toy_by_id(toy_id)
    return updated_toy


def update_toy_price_by_id(toy_id: int, new_price: float) -> Toy | None:
    """
    Updates the toy's price in the database based on the given ID
    :param toy_id: The ID of the toy in the database
    :param new_price: The new price of the toy in the database
    :return: The updated toy in the database that matches the given ID.
    If there is no toy matching the given ID, the method returns None
    """

    toy_to_update = get_toy_by_id(toy_id)
    if not toy_to_update:
        return None

    connection, cursor = open_conn_and_cursor()

    cursor.execute(
        "UPDATE toys SET price = %s WHERE toy_id = %s",
        (new_price, toy_id)
    )

    connection.commit()

    close_conn_and_cursor(connection, cursor)

    updated_toy = get_toy_by_id(toy_id)
    return updated_toy


def remove_toy_by_id(toy_id: int) -> Toy | None:
    """
    Removes the toy in the database based on the given ID
    :param toy_id: The ID of the toy in the database
    :return: The removed toy in the database that matches the given ID.
    If there is no toy matching the given ID, the method returns None
    """

    toy_to_remove = get_toy_by_id(toy_id)
    if not toy_to_remove:
        return None

    connection, cursor = open_conn_and_cursor()


    cursor.execute(
        "DELETE FROM toys WHERE toy_id = %s",
        (toy_id,)
    )

    connection.commit()

    close_conn_and_cursor(connection, cursor)

    return toy_to_remove


def remove_all_toys() -> list[Toy] | None:
    """
    Removes all the toys in the database
    :return: All the removed toys in the database. If there are no toys, it returns None
    """
    toys_to_remove = get_all_toys()
    if not toys_to_remove:
        return None

    connection, cursor = open_conn_and_cursor()

    cursor.execute("TRUNCATE TABLE toys")

    connection.commit()

    close_conn_and_cursor(connection,cursor)

    return toys_to_remove
