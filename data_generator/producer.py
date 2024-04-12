# Purpose: Produces products, streaming sales transactions, and restocking activities to Kafka topics
# Author:  Gary A. Stafford
# Date: 2022-08-29
# Instructions: Modify the configuration.ini file to meet your requirements.

import os
import configparser
import json
import random
import time
from csv import reader
from datetime import datetime
from models.product import Product
from models.sale import Sale
from models.inventory import Inventory
from models.customer import pick_customer

config = configparser.ConfigParser(inline_comment_prefixes=('#'))
config.read("data_generator/configuration.ini")

# *** CONFIGURATION ***
min_sale_freq = int(config["SALES"]["min_sale_freq"])
max_sale_freq = int(config["SALES"]["max_sale_freq"])
number_of_sales = int(config["SALES"]["number_of_sales"])
transaction_quantity_one_item_freq = int(config["SALES"]["transaction_quantity_one_item_freq"])
item_quantity_one_freq = int(config["SALES"]["item_quantity_one_freq"])
member_freq = int(config["SALES"]["member_freq"])
club_member_discount = float(config["SALES"]["club_member_discount"])
add_supp_freq_group1 = int(config["SALES"]["add_supp_freq_group1"])
add_supp_freq_group2 = int(config["SALES"]["add_supp_freq_group2"])
supplements_cost = float(config["SALES"]["supplements_cost"])
min_inventory = int(config["INVENTORY"]["min_inventory"])
restock_amount = int(config["INVENTORY"]["restock_amount"])
keep_existing_price = float(config["PRODUCT"]["keep_existing_price"])
maximum_pct_price_increase = float(config["PRODUCT"]["maximum_pct_price_increase"])

# *** VARIABLES ***
customers = []
products = []
propensity_to_buy_range = []

# create products and propensity_to_buy lists from CSV data file
def create_product_list():
    with open("data_generator/models/products.csv", "r") as csv_file:
        next(csv_file)  # skip header row
        csv_reader = reader(csv_file)
        csv_products = list(csv_reader)

    for p in csv_products:
        new_product = Product(
            str(datetime.now()),
            p[0],
            p[1],
            p[2],
            p[3],
            p[4],
            p[5],
            p[6],
            to_bool(p[7]),
            to_bool(p[8]),
            to_bool(p[9]),
            to_bool(p[10]),
            p[14],
        )
        products.append(new_product)

        new_product.write_to_json()
        print(new_product)

        propensity_to_buy_range.append(int(p[14]))
    propensity_to_buy_range.sort()


# generate synthetic sale transactions
def generate_sales():
    
    # common to all transactions
    range_min = propensity_to_buy_range[0]
    range_max = propensity_to_buy_range[-1]

    # generate a number of sales
    for _ in range(0, number_of_sales):
        
        # choose existing customer or generate new
        customer = pick_customer(customers)
        customer.write_to_json()
        print(customer)

        # append customer to list of customers or overwrite previous info if neccessary
        if customer.customer_id > len(customers):
            customers.append(customer)
        else:
            customers[customer.customer_id - 1] = customer

        # reset values
        rnd_propensity_to_buy = -1
        previous_rnd_propensity_to_buy = -1

        # generate a number of transactions per sale
        for _ in range(0, random_transaction_item_quantity()):
            
            # reduces but not eliminates risk of duplicate products in same transaction
            if rnd_propensity_to_buy == previous_rnd_propensity_to_buy:
                rnd_propensity_to_buy = closest_product_match(
                    propensity_to_buy_range, random.randint(range_min, range_max)
                )
            previous_rnd_propensity_to_buy = rnd_propensity_to_buy
            
            for p_idx, p in enumerate(products):
                if p.propensity_to_buy == rnd_propensity_to_buy:
                    
                    # check if price should be increased
                    if random.uniform(0, 1) > keep_existing_price:
                        p.price *= 1 + random.uniform(0, maximum_pct_price_increase)
                        p.write_to_json()
                        print(p)

                    # generate new sale
                    new_sale = Sale(
                        customer_id=customer.customer_id,
                        product_id=p.product_id,
                        price=p.price,
                        quantity=random_quantity(),
                        is_member=random_club_member(),
                        add_supplements=random_add_supplements(p.product_id),
                    )

                    print(new_sale)
                    new_sale.write_to_json()

                    p.inventory_level = p.inventory_level - new_sale.quantity
                    if p.inventory_level <= min_inventory:
                        restock_item(p.product_id)
                    break
        
        # wait a certain amount of time
        time.sleep(random.randint(min_sale_freq, max_sale_freq))


# restock inventories
def restock_item(product_id):
    for p in products:
        if p.product_id == product_id:
            new_level = p.inventory_level + restock_amount
            new_inventory = Inventory(
                str(datetime.now()),
                p.product_id,
                p.inventory_level,
                restock_amount,
                new_level,
            )
            p.inventory_level = new_level  # update existing product item
            
            print(new_inventory)
            new_inventory.write_to_json()
            break


# convert uppercase boolean values from CSV file to Python
def to_bool(value):
    if type(value) == str and str(value).lower() == "true":
        return True
    return False


# find the closest match in propensity_to_buy_range range
# Credit: https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
def closest_product_match(lst, k):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]


# individual item purchase quantity (usually 1, max 3)
def random_quantity():
    rnd = random.randint(1, 30)
    if rnd == 30:
        return 3
    if rnd <= item_quantity_one_freq:
        return 1
    return 2


# transaction items quantity (usually 1, max 3)
def random_transaction_item_quantity():
    rnd = random.randint(1, 20)
    if rnd >= 19:
        return 3
    if rnd <= transaction_quantity_one_item_freq:
        return 1
    return 2


# smoothie club membership? (usually False)
def random_club_member():
    rnd = random.randint(1, 10)
    if rnd <= member_freq:
        return True
    return False


# add supplements? (more frequently purchased for SF and SC products)
def random_add_supplements(product_id):
    rnd = random.randint(1, 10)
    if str(product_id).startswith("SF") or str(product_id).startswith("SC"):
        if rnd <= add_supp_freq_group1:
            return True
        return False
    if rnd <= add_supp_freq_group2:
        return True
    return False


if __name__ == "__main__":

    os.makedirs("data/customer", exist_ok=True)
    os.makedirs("data/product", exist_ok=True)
    os.makedirs("data/sales", exist_ok=True)
    os.makedirs("data/inventory", exist_ok=True)

    create_product_list()
    generate_sales()
