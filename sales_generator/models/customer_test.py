from faker import Faker


if __name__ == "__main__":

    fake = Faker()
    # fake.seed_instance(1337)


    print(fake.name())
    print(fake.address())
    print(fake.phone_number())
    print(fake.email())
    print(fake.credit_card_number())
    print(fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y"))

    print(fake.company())
    print(fake.job())



