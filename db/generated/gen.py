from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 50
num_products = 2000
num_purchases = 2500
num_sellers = 10
num_cart_items = 100
num_forsale_items = 1000
num_product_ratings = 1000
num_seller_ratings = 5

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    uids = []
    with open('db/generated/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.address()
            balance = round(random.uniform(0, 10000), 2)
            date = fake.date_between("2000-01-01")
            writer.writerow([uid, email, firstname, lastname, password, address, balance, date])
            uids.append(uid)
        print(f'{num_users} generated')
    return uids


def gen_sellers(num_sellers, num_users):
    s_uids = []
    with open('db/generated/Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for i in range(num_sellers):
            if i % 5 == 0:
                print(f'{i}', end=' ', flush=True)
            s_uid = fake.unique.random_int(min=1, max=num_users)
            s_uids.append(s_uid)
            writer.writerow([s_uid])
        print(f'{num_sellers} generated')
    return s_uids


def gen_products(num_products):
    available_pids = []
    with open('db/generated/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_carts(num_cart_items, uids, s_uids, available_pids):
    with open('db/generated/Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for i in range(num_cart_items):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            pid = fake.random_element(elements=available_pids)
            s_uid = fake.random_element(elements=s_uids)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([i, uid, pid, s_uid, quantity])
        print(f'{num_cart_items} generated')
    return 

def gen_forsales(num_forsale_items, s_uids, available_pids):
    with open('db/generated/ForSales.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ForSales...', end=' ', flush=True)
        for i in range(num_forsale_items):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids)
            s_uid = fake.random_element(elements=s_uids)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([pid, s_uid, price, quantity])
        print(f'{num_forsale_items} generated')
    return 


def gen_purchases(num_purchases, available_pids, uids):
    with open('db/generated/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_prod_ratings(num_product_ratings, available_pids, uids):
    with open('db/generated/ProductRatings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Ratings...', end=' ', flush=True)
        for i in range(num_product_ratings):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids)
            uid = fake.random_element(elements=uids)
            rating = fake.random_int(min=1, max=5)
            writer.writerow([pid, uid, rating])
        print(f'{num_product_ratings} generated')
    return

def gen_seller_ratings(num_seller_ratings, s_uids, uids):
    with open('db/generated/SellerRatings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Ratings...', end=' ', flush=True)
        for i in range(num_product_ratings):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            s_uid = fake.random_element(elements=s_uids)
            uid = fake.random_element(elements=uids)
            rating = fake.random_int(min=1, max=5)
            writer.writerow([s_uid, uid, rating])
        print(f'{num_seller_ratings} generated')
    return


uids = gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids, uids)
s_uids = gen_sellers(num_sellers, num_users)
gen_carts(num_cart_items, uids, s_uids, available_pids)
gen_purchases(num_purchases, available_pids, uids)
gen_prod_ratings(num_product_ratings, available_pids, uids)
gen_seller_ratings(num_seller_ratings, s_uids, uids)
