"""
This file has the main method that is being run when running the app
"""
from app.data_analytics import show_tables
from app.services import toy_service as toy_serv
import app.utils.db_connection_util as conn


def main():
    """
    The main method that is being run when running the app
    """

    conn.setup()

    print("""
    
    *~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~||~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*
                 Welcome to the Toy Warehouse Management App!
    *~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~||~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*
    
    
    """)

    in_use = True

    while in_use:
        print("Which operation do you want to do on the toy database?")
        print("Please enter your choice (1-11): ")
        print("""
        [1] Add a toy
        [2] Remove a toy
        [3] Remove all toys
        [4] Change toy name
        [5] Change toy price
        [6] Get toy by id
        [7] Get all toys 
        [8] Get all toys by price cap
        [9] Get all toys by manufacturer
        [10] Show data tables
        [11] Exit
        """)
        command_input = input(">>> ")

        match command_input:
            case "1": # Add a toy
                name = input("Enter the name of the new toy: ")
                manufacturer = input("Enter the manufacturer of the new toy: ")
                weight = toy_serv.ask_for_float("Enter the weight of the new toy in grams: ")
                price = toy_serv.ask_for_float("Enter the price of the new toy in USD: ")
                units_sold = toy_serv.ask_for_int("Enter the number of units sold of the new toy: ")

                added_toy = toy_serv.create_toy(name, manufacturer, weight, price, units_sold)
                print(added_toy)

            case "2": # Remove a toy
                toy_id = toy_serv.ask_for_int("Enter ID of toy to be removed: ")

                removed_toy = toy_serv.remove_toy_by_id(toy_id)
                print(removed_toy)

            case "3": # Remove all toys
                removed_toys = toy_serv.remove_all_toys()
                print(removed_toys)

            case "4": # Change toy name
                toy_id = toy_serv.ask_for_int("Enter ID of toy to be changed name: ")
                new_name = input("Enter new name: ")
                print(toy_serv.change_toy_name(toy_id, new_name))

            case "5": # Change toy price
                toy_id = toy_serv.ask_for_int("Enter ID of toy to be changed price: ")
                new_price = toy_serv.ask_for_float("Enter new price in USD: ")
                print(toy_serv.change_toy_price(toy_id, new_price))


            case "6": # Get toy by id
                toy_id = toy_serv.ask_for_int("Enter ID of toy: ")
                print(toy_serv.get_toy_by_id(toy_id))

            case "7": # Get all toys
                results = toy_serv.get_all_toys()
                print(results)

            case "8": # Get all toys by price cap7

                price_cap = toy_serv.ask_for_float("Enter price cap: ")
                results = toy_serv.get_all_toys_by_price_cap(price_cap)
                print(results)

            case "9": # Get all toys by manufacturer
                manufacturer = input("Enter manufacturer name: ")
                results = toy_serv.get_all_toys_by_manufacturer(manufacturer)
                print(results)

            case "10": # Show data tables
                show_tables()

            case "11": # Exit
                print("Goodbye.")
                in_use = False

            case _:
                print("Must be a number between 1-11")

        print("\n")


if __name__=="__main__":
    main()
