import os
import json
from datetime import datetime

class Product:
    def __init__(
        self,
        event_time: str,
        product_id: str,
        category: str,
        item: str,
        size: str,
        cogs: float,
        price: float,
        inventory_level: int,
        contains_fruit: bool,
        contains_veggies: bool,
        contains_nuts: bool,
        contains_caffeine: bool,
        propensity_to_buy: int,
    ):
        self.event_time = str(event_time)
        self.product_id = str(product_id)
        self.category = str(category)
        self.item = str(item)
        self.size = str(size)
        self.cogs = float(cogs)
        self.price = float(price)
        self.inventory_level = int(inventory_level)
        self.contains_fruit = bool(contains_fruit)
        self.contains_veggies = bool(contains_veggies)
        self.contains_nuts = bool(contains_nuts)
        self.contains_caffeine = bool(contains_caffeine)
        self.propensity_to_buy = int(propensity_to_buy)

    def __str__(self):
        return (
            "\nProduct created: \tproduct_id: {0}, category: {1}, item: {2}, size: {3}, price: ${4:.2f}".format(
                self.product_id,
                self.category,
                self.item,
                self.size,
                self.price
            )
        )

    def write_to_json(self):

        # Serializing json
        json_object = json.dumps([{
            "event_time": self.event_time,
            "product_id": self.product_id,
            "category": self.category,
            "item": self.item,
            "size": self.size,
            "cogs": self.cogs,
            "price": self.price,
            "contains_fruit": self.contains_fruit,
            "contains_veggies": self.contains_veggies,
            "contains_nuts": self.contains_nuts,
            "contains_caffeine": self.contains_caffeine
        }])
        
        # Writing to sample.json
        file_path = os.path.join("data", "product", f"{int(datetime.now().timestamp() * 1e6)}.json")
        with open(file_path, "w") as outfile:
            outfile.write(json_object)
