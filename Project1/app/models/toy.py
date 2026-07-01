"""
Pydantic model for toy database entries.
"""

from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints

NonBlankStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

class Toy(BaseModel):
    """
    The model class of the toy database entries
    """
    toy_id : Annotated[int, Field(gt=0)]
    name: NonBlankStr
    manufacturer:NonBlankStr
    weight: Annotated[float, Field(gt=0)]
    price: Annotated[float, Field(ge=0)]
    units_sold: Annotated[int, Field(ge=0)]

    def __str__(self):
        return (f"Toy(ID:{self.toy_id}, "
                f"Name: {self.name}, "
                f"Manufacturer: {self.manufacturer}, "
                f"Weight: {self.weight}g, "
                f"Price: ${self.price:.2f}, "
                f"Number of Units Sold: {self.units_sold})")
