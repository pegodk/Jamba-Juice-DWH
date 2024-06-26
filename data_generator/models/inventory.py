import os
import json
from datetime import datetime

class Inventory:
    def __init__(
        self,
        event_time: str,
        product_id: str,
        existing_level: int,
        stock_quantity: int,
        new_level: int,
    ):
        self.event_time = str(event_time)
        self.product_id = str(product_id)
        self.existing_level = int(existing_level)
        self.stock_quantity = int(stock_quantity)
        self.new_level = int(new_level)

    def __str__(self):
        return (
            "\nRestocking inventory: \tproduct_id: {0}, existing_level: {1:.0f}, stock_quantity: {2:.0f}, new_level: {3:.0f}".format(
                self.product_id,
                self.existing_level,
                self.stock_quantity,
                self.new_level,
            )
        )


    def write_to_json(self):

        # Serializing json
        json_object = json.dumps([{
            "event_time": self.event_time,
            "product_id": self.product_id,
            "existing_level": self.existing_level,
            "stock_quantity": self.stock_quantity,
            "new_level": self.new_level
        }])
        
        # Writing to sample.json
        file_path = os.path.join("data", "inventory", f"{int(datetime.now().timestamp() * 1e6)}.json")
        with open(file_path, "w") as outfile:
            outfile.write(json_object)