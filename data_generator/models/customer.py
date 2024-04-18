import os
import json
import configparser
import random
from datetime import datetime
from faker import Faker
fake = Faker()

config = configparser.ConfigParser(inline_comment_prefixes=('#'))
config.read("data_generator/configuration.ini")
returning_customers = float(config["CUSTOMER"]["returning_customers"])
persistant_address = float(config["CUSTOMER"]["persistant_address"])
persistant_credit_card = float(config["CUSTOMER"]["persistant_credit_card"])

def pick_customer(ls_customers):

    # Initialize save flag to false
    save_new_entry_flag = False

    # choose existing customer or generate new
    if len(ls_customers) == 0 or (random.uniform(0, 1) > returning_customers):
        customer = Customer(customer_id=len(ls_customers) + 1)
        save_new_entry_flag = True
    else:
        cust_idx = random.randint(0, len(ls_customers) - 1)
        customer = ls_customers[cust_idx]

        if random.uniform(0, 1) > persistant_address:
            customer.address = fake.address()
            save_new_entry_flag = True

        if random.uniform(0, 1) > persistant_credit_card:
            customer.credit_card_number = fake.credit_card_number()
            customer.credit_card_expire = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
            save_new_entry_flag = True

    # Save customer to file only if new customer or changes to existing
    if save_new_entry_flag:
        customer.write_to_json()
        print(customer)

    return customer

class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.full_name = fake.name()
        self.address = fake.address()
        self.phone_number = fake.phone_number()
        self.email = fake.email()
        self.credit_card_number = fake.credit_card_number()
        self.credit_card_expire = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")

    def __str__(self):
        return (
            "\nCustomer: \t\tcustomer_id: {}, full_name: {}, email: {}".format(
                self.customer_id,
                self.full_name,
                self.email
            )
        )

    def write_to_json(self):

        # Serializing json
        json_object = json.dumps([{
            "event_time": str(datetime.now()),
            "customer_id": self.customer_id,
            "full_name": self.full_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "credit_card_number": self.credit_card_number,
            "credit_card_expire": self.credit_card_expire
        }])
        
        # Writing to sample.json
        file_path = os.path.join("data", "customer", f"{int(datetime.now().timestamp() * 1e6)}.json")
        with open(file_path, "w") as outfile:
            outfile.write(json_object)

if __name__ == "__main__":

    customers = []

    for _ in range(10):
        customer = pick_customer(customers)
        
        print(customer)
        customers.append(customer)
