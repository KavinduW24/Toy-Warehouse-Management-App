"""
This contains code for the data analytics of the toys
"""
from matplotlib.ticker import StrMethodFormatter
import pandas as pd
import matplotlib.pyplot as plt
from app.repositories import toy_repository



def show_tables():
    """
    It processes and displays the data in the database
    """

    connection, cursor = toy_repository.open_conn_and_cursor()

    df = pd.DataFrame(pd.read_sql("SELECT * FROM toys", connection))

    toy_repository.close_conn_and_cursor(connection, cursor)

    plt.figure(figsize=(8, 5))
    plt.bar(df["name"], df["units_sold"])

    plt.title("Units Sold by Toy")
    plt.xlabel("Toy")
    plt.ylabel("Units Sold")
    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    manufacturer_sales = (
        df.groupby("manufacturer")["units_sold"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(8, 8))
    plt.pie(
        manufacturer_sales["units_sold"],
        labels=manufacturer_sales["manufacturer"],
        autopct="%1.1f%%"
    )

    plt.title("Units Sold by Manufacturer")
    plt.legend()
    plt.show()

    df_sorted = df.sort_values("price")

    plt.figure(figsize=(8, 5))
    plt.plot(
        df_sorted["name"],
        df_sorted["price"],
        marker="o"
    )

    plt.title("Toy Prices")
    plt.xlabel("Toy")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)

    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))

    plt.tight_layout()
    plt.show()

    total_revenue_per_toy = df["price"] * df["units_sold"]

    plt.bar(df["name"],total_revenue_per_toy, color = "orange")

    plt.title("Total Revenue By Toys")
    plt.xlabel("Toy")
    plt.ylabel("Total Revenue (USD)")
    plt.xticks(rotation=45)

    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))

    plt.tight_layout()

    plt.show()
