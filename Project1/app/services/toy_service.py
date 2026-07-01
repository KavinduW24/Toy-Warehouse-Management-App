"""
The layer that interacts with the user interface and
handles all business logic between the user’s commands and the repository.
"""
from pydantic import ValidationError

from app.models.toy import Toy
from app.repositories import toy_repository

def ask_for_int(prompt:str) -> int:
    """
    Asks the user for a valid positive integer.
    Prompt must not be blank.

    :param prompt: Message displayed to the user
    :return: Integer that the user did input
    """

    if not (prompt and prompt.strip()): # if the prompt is empty
        return -1

    is_valid_integer = False
    user_int = 0
    while not is_valid_integer:
        try:
            user_int = int(input(prompt))
            is_valid_integer = True
        except ValueError:
            print(f"Invalid input. {user_int} is not an whole number")
        print("\n")
    return user_int


def ask_for_float(prompt:str) -> float:
    """
    Asks the user for a valid float.
    Prompt must not be blank.

    :param prompt: Message displayed to the user
    :return: Float that the user did input
    """

    if not (prompt and prompt.strip()): # if the prompt is empty
        return -1

    is_valid_float = False
    user_float = 0
    while not is_valid_float:
        try:
            user_float = float(input(prompt))
            is_valid_float = True
        except ValueError:
            print(f"Invalid input. {user_float} is not an number")
        print("\n")
    return user_float


def get_toy_by_id(toy_id: int) -> str:
    """
    Gets the toy from the database based on the given ID
    :param toy_id: The ID of the toy wanted in the database
    :return: A string showing confirmation or failure to retrieve
    the toy of the specified ID in the database
    """
    toy = toy_repository.get_toy_by_id(toy_id)
    if not toy:
        return f"There is no toy by ID {toy_id}"
    return f"Got {toy} from database"


def get_all_toys() -> str:
    """
    Gets all the toys in the database
    :return: A string showing of all the toys in the database
    """
    results = toy_repository.get_all_toys()

    if not results:
        return "There are no toys in the database"

    return "All toys in the database:\n" + "\n".join(str(toy) for toy in results)


def get_all_toys_by_price_cap(price_cap: float) -> str:
    """
    Gets all the toys in the database at or below the given price cap
    :param price_cap: The cap that all toys are less than or equal to in the database
    :return: A string showing of all the toys in the database at or below the given price cap
    """
    results = toy_repository.get_all_toys_by_price_cap(price_cap)

    if not results:
        return f"There are no toys in the database that are less than or equal to ${price_cap:.2f}"

    return (f"All toys in the database at or below ${price_cap:.2f}:\n"
            + "\n".join(str(toy) for toy in results))


def get_all_toys_by_manufacturer(manufacturer: str) -> str:
    """
    Gets all the toys in the database from the give manufacturer
    :param manufacturer: The manufacturer of toys in the database
    :return: A string showing of all the toys in the database from the give manufacturer
    """
    results = toy_repository.get_all_toys_by_manufacturer(manufacturer)

    if not results:
        return f"There are no toys in the database that are made by {manufacturer}"

    return  (f"All toys in the database from {manufacturer}:\n"
             + "\n".join(str(toy) for toy in results))


def create_toy(name: str, manufacturer: str, weight: float, price: float, units_sold:int) -> str:
    """
    Adds a new toy in the database
    :param name: The name of the new toy in the database.
    Must not be blank

    :param manufacturer: The manufacturer of the new toy in the database.
    Must not be blank

    :param weight: The weight of the new toy in the database.
    Must be a positive number above zero

    :param price: The price of the new toy in the database.
    Must be a number greater than or equal to zero

    :param units_sold: The number of units sold of the new toy in the database.
    Must be a number greater than or equal to zero

    :return: A string that shows confirmation or failure
    of the creation of a new toy in the database
    """
    existing_toys = toy_repository.get_all_toys()

    if not existing_toys :
        toy_id = 1
    else:
        toy_id = max(toy.toy_id for toy in existing_toys) + 1

    try:
        toy = Toy(toy_id = toy_id, name = name, manufacturer = manufacturer,
                  weight = weight, price = price, units_sold = units_sold)
        toy_repository.add_toy(toy)
        return f"{toy} is added to the database"
    except ValidationError as e:
        return (f"Toy(ID:{toy_id}, "
        f"Name: {name}, "
        f"Manufacturer: {manufacturer}, "
        f"Weight: {weight}g, "
        f"Price: ${price:.2f}, "
        f"Number of Units Sold: {units_sold}) "
        f"was not added because of these validation errors\n{e}")


def remove_toy_by_id(toy_id: int) -> str:
    """
    Removes the toy in the database based on the given ID
    :param toy_id: The ID of the toy in the database
    :return: A string showing the confirmation or failure to remove the given toy in the database
    """
    result = toy_repository.remove_toy_by_id(toy_id)

    if not result:
        return f"Toy with ID {toy_id} not found! Try again!"

    return f"Toy #{toy_id} removed: {result}"


def change_toy_name(toy_id: int, new_name: str) -> str:
    """
    Changes the toy with the given id's name to the given name
    :param toy_id: The ID of the toy in the database
    :param new_name: The new name of the toy in the database. Must not be blank
    :return: A string showing confirmation or failure of the toy's name being updated
    """
    if not (new_name and new_name.strip()): # if the new name is empty
        return "The new name cannot be blank"

    result = toy_repository.update_toy_name_by_id(toy_id,new_name)

    if not result:
        return f"Toy with ID {toy_id} not found! Try again!"

    return f"Toy #{toy_id} name updated: {result}"


def change_toy_price(toy_id: int, new_price: float) -> str:
    """
    Changes the toy with the given id's price to the given price
    :param toy_id: The ID of the toy in the database
    :param new_price: The new price of the toy in the database. Must not be blank
    :return: A string showing confirmation or failure of the toy's price being updated
    """
    if new_price < 0:
        return "The new price must be greater than or equal to zero"

    result = toy_repository.update_toy_price_by_id(toy_id,new_price)

    if not result:
        return f"Toy with ID {toy_id} not found! Try again!"

    return f"Toy #{toy_id} price updated: {result}"


def remove_all_toys() -> str:
    """
    Removes all toys from the database
    :return: A string showing confirmation or failure to remove toys in the database
    """
    result = toy_repository.remove_all_toys()
    if not result:
        return "There are no toys in the database to remove"

    return f"Removed all {len(result)} toys in the database"
