import os
import sys
from pizzeria.models import Size, Topping
from pizzeria.serializers import ToppingSerializer, SizeSerializer


def init_db():
    sizes = [
        {"name": "small", "price": "9.00"},
        {"name": "medium", "price": "12.00"},
        {"name": "large", "price": "15.00"},
    ]

    toppings = [
        {"name": "margarita", "price": "0.00"},
        {"name": "marinara", "price": "1.00"},
        {"name": "salami", "price": "2.00"},
    ]

    # DB can be initialized in this script to insert all the initial values automatically.


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slicebites.settings")
    init_db()
