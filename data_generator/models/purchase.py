import os
import json
import configparser
from datetime import datetime

config = configparser.ConfigParser(inline_comment_prefixes=('#'))
config.read("data_generator/configuration.ini")
club_member_discount = float(config["SALES"]["club_member_discount"])
supplements_cost = float(config["SALES"]["supplements_cost"])

class Purchase:
    def __init__(
        self,
        customer_id: int,
        product_id: int,
        price: float,
        quantity: int,
        is_member: bool,
        add_supplements: bool,
    ):
        self.customer_id = customer_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.member_discount = club_member_discount if is_member else 0.00
        self.supplement_price = supplements_cost if add_supplements else 0.0
        self.total_purchase = self.quantity * (self.price + self.supplement_price)
        self.total_purchase = self.total_purchase * (1 - self.member_discount)
        self.total_purchase = round(self.total_purchase, 2)

    def __str__(self):
        return (
            "\nPurchase: \t\tproduct_id: {0}, quantity: {1:.0f}, supplement_price: ${2:.2f}, member_discount: {3:.0%}, total: ${4:.2f}".format(
                self.product_id,
                self.quantity,
                self.supplement_price,
                self.member_discount,
                self.total_purchase,
            )
        )

    def write_to_json(self):

        # Serializing json
        json_object = json.dumps([{
            "transaction_time": str(datetime.now()),
            "transaction_id": str(abs(hash(str(datetime.now())))),
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "supplement_price": self.supplement_price,
            "member_discount": self.member_discount,
            "total_purchase": self.total_purchase
        }])
        
        # Writing to sample.json
        file_path = os.path.join("data", "purchase", f"{int(datetime.now().timestamp() * 1e6)}.json")
        with open(file_path, "w") as outfile:
            outfile.write(json_object)