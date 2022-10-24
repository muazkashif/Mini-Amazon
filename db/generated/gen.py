from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import datetime

num_users = 15
num_products = 2000
num_purchases = 2500
num_sellers = 5
num_cart_items = 100
num_forsale_items = 50
num_product_ratings = 400
num_seller_ratings = 5
num_ratings = 100

file_path = "../data/"

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    uids = []
    with open(file_path + 'Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = fake.email()
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.address()
            balance = round(random.uniform(0, 10000), 2)
            date = fake.date_between(datetime.datetime(2000, 1, 1))
            writer.writerow([uid, email, password, firstname, lastname, address, balance, date])
            uids.append(uid)
        print(f'{num_users} generated')
    return uids


def gen_sellers(num_sellers, User_IDs):
    s_uids = []
    with open(file_path + 'Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for i in range(num_sellers):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = fake.random_element(elements=User_IDs)
            while uid in s_uids:
                uid = fake.random_element(elements=User_IDs)
            writer.writerow([uid])
            s_uids.append(uid)
        print(f'{num_sellers} generated')
    return s_uids


def gen_products(num_products):
    available_pids = []
    with open(file_path + 'Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            pname = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            rating = round(random.uniform(0.0,5.0),2)
            descriptions = fake.sentence() 
            category = fake.sentence(nb_words = 2)[:-1]
            images = fake.binary(length = 64) #Might be better generated some other way
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, pname, category, descriptions, images, price, rating, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_carts(num_cart_items, uids, s_uids, available_pids):
    with open(file_path + 'Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for i in range(num_cart_items):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            pid = fake.random_element(elements=available_pids)
            s_uid = fake.random_element(elements=s_uids)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([uid, pid, s_uid, quantity])
        print(f'{num_cart_items} generated')
    return 

def gen_forsales(num_forsale_items, s_uids, available_pids):
    already_done_keys = [()]
    with open(file_path + 'ForSaleItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ForSales...', end=' ', flush=True)
        for i in range(num_forsale_items):
            print(f'{i}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids)
            s_uid = fake.random_element(elements=s_uids)
            key = (pid,s_uid)
            while key in already_done_keys:
                pid = fake.random_element(elements=available_pids)
                s_uid = fake.random_element(elements=s_uids)
            quantity = fake.random_int(min=1, max=10)
            writer.writerow([pid, s_uid, quantity])
            already_done_keys.append(key)
        print(f'{num_forsale_items} generated')
    return 


def gen_transactions(num_purchases, available_pids, uids,sids):
    order_status = ["Received","Processing","Shipped","Delivered"]
    with open(file_path + 'Transactions.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            sid = fake.random_element(elements=sids)
            pid = fake.random_element(elements=available_pids)
            quant = fake.random_int(min = 1, max = 5) #CHANGE MAX TO TAKE INTO ACCOUNT STALK
            time_purchased = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
            status = fake.random_element(elements = order_status)
            writer.writerow([uid, sid, pid, quant, time_purchased, status])
        print(f'{num_purchases} generated')
    return

def gen_prod_ratings(num_product_ratings, available_pids, uids):
    # already_done_keys = [()]
    with open(file_path + 'ProductRatings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Ratings...', end=' ', flush=True)
        for i in range(num_product_ratings):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids)
            uid = fake.random_element(elements=uids)
            key = (uid,pid)
            # if i == 230:
            #     print("start debugging")
            # while key in already_done_keys:
            #     pid = fake.random_element(elements=available_pids)
            #     uid = fake.random_element(elements=uids)
            rating = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=10)
            time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
            writer.writerow([uid, pid, rating,review,time])
            # already_done_keys.append(key)
        print(f'{num_product_ratings} generated')
    return

def gen_seller_ratings(num_seller_ratings, s_uids, uids):
    already_done_keys = [[]]
    with open(file_path + 'SellerRatings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Ratings...', end=' ', flush=True)
        for i in range(num_seller_ratings):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            s_uid = fake.random_element(elements=s_uids)
            uid = fake.random_element(elements=uids)
            key = (uid,s_uid)
            while key in already_done_keys:
                s_uid = fake.random_element(elements=s_uids)
                uid = fake.random_element(elements=uids)
            rating = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=10)
            time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
            writer.writerow([uid, s_uid, rating,review,time])
            already_done_keys.append(key)
        print(f'{num_seller_ratings} generated')
    return

def gen_ratings(num_ratings, s_uids, uids, available_pids):
    already_done_keys = [[]]
    with open(file_path + 'Ratings.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Ratings...', end=' ', flush=True)
        for i in range(num_ratings):
            if i % 5 == 0:
                print(f'{i}', end=' ', flush=True)
            s_uid = fake.random_element(elements=s_uids)
            pid = fake.random_element(elements=available_pids)
            uid = fake.random_element(elements=uids)
            key = (uid,s_uid, pid)
            while key in already_done_keys:
                pid = fake.random_element(elements=available_pids)
                s_uid = fake.random_element(elements=s_uids)
                uid = fake.random_element(elements=uids)
            rating = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=10)
            time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
            writer.writerow([uid, s_uid, pid, rating,review,time])
            already_done_keys.append(key)
        print(f'{num_ratings} generated')
    return

if __name__ == "__main__":
    uids = gen_users(num_users)
    available_pids = gen_products(num_products)
    # gen_transactions(num_purchases, available_pids, uids)
    s_uids = gen_sellers(num_sellers, uids)
    gen_carts(num_cart_items, uids, s_uids, available_pids)
    gen_transactions(num_purchases, available_pids, uids,s_uids)
    #gen_prod_ratings(num_product_ratings, available_pids, uids)
    #gen_seller_ratings(num_seller_ratings, s_uids, uids)
    gen_forsales(num_forsale_items, s_uids, available_pids)
    gen_ratings(num_ratings, s_uids, uids, available_pids)
