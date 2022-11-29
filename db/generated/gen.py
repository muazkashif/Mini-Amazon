from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import datetime

num_users = 1000
num_products = 10000
num_purchases = 5000
num_sellers = 1000
num_cart_items = 4000
num_forsale_items = 4000
num_ratings = 5000



file_path = "../data/"

categories = ["Travel", "Personal_Care", "Kitchenware", "Furniture", "Electronics", "Sports", "Toiletries", "Clothing", "Books", "School"]

Faker.seed(0)
fake = Faker()
# dict_of_rated_prods = {}

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def get_csv_reader(r):
    return csv.reader(r, dialect='unix')


def gen_users(num_users):
    uids = []
    emails = []
    with open(file_path + 'Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        plain_password = f'abcd'
        password = generate_password_hash(plain_password)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = str(uid) + "@exmaple.com"
            # while email in emails:
            #     email = fake.email()
            # plain_password = f'pass{uid}'
            # password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.address()
            balance = round(random.uniform(0, 10000), 2)
            date = fake.date_between(datetime.datetime(2000, 1, 1))
            writer.writerow([uid, email, password, firstname, lastname, address, balance, date])
            uids.append(uid)
            emails.append(email)
        print(f'{num_users} generated')
    return uids


def gen_sellers(num_sellers):
    s_uids = []
    uids = []
    for i in range(num_users):
        uids.append(i)
    print("DONE READING")
    with open(file_path + 'Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for i in range(num_sellers):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            while uid in s_uids:
                uid = fake.random_element(elements=uids)
            writer.writerow([uid])
            s_uids.append(uid)
        print(f'{num_sellers} generated')
    return s_uids,uids


# def gen_products(num_products):
#     available_pids = []
#     names = []
#     with open(file_path + 'Products.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Products...', end=' ', flush=True)
#         for pid in range(num_products):
#             if pid % 100 == 0:
#                 print(f'{pid}', end=' ', flush=True)
#             pname = fake.sentence(nb_words=4)[:-1]
#             while pname in names:
#                 pname = fake.sentence(nb_words=4)[:-1]
#             price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
#             available = fake.random_element(elements=('true', 'true', 'true', 'true', 'false'))
#             rating = round(random.uniform(0.0,5.0),2)
#             descriptions = fake.sentence() 
#             category = categories[fake.random_int(min = 0, max = len(categories) - 1)]
#             images = fake.binary(length = 64) #Might be better generated some other way
#             names.append(pname)
#             if available == 'true':
#                 available_pids.append(pid)
#             writer.writerow([pid, pname, category, descriptions, images, price, rating, available])
#         print(f'{num_products} generated; {len(available_pids)} available')
#     return available_pids


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


        # for i in range(num_forsale_items):
        #     print(f'{i}', end=' ', flush=True)
        #     pid = fake.random_element(elements=available_pids)
        #     s_uid = fake.random_element(elements=s_uids)
        #     key = (pid,s_uid)
        #     while key in already_done_keys:
        #         pid = fake.random_element(elements=available_pids)
        #         s_uid = fake.random_element(elements=s_uids)
        #     quantity = fake.random_int(min=1, max=10)
        #     writer.writerow([pid, s_uid, quantity])
        #     already_done_keys.append(key)
        # print(f'{num_forsale_items} generated')
    #return 


def gen_transactions(num_purchases, available_pids, uids,sids):
    order_status = ["Received","Processing","Shipped","Delivered"]
    with open(file_path + 'Transactions.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 10 == 0:
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

# def gen_prod_ratings(num_product_ratings, available_pids, uids):
#     # already_done_keys = [()]
#     with open(file_path + 'ProductRatings.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Product Ratings...', end=' ', flush=True)
#         for i in range(num_product_ratings):
#             if i % 10 == 0:
#                 print(f'{i}', end=' ', flush=True)
#             pid = fake.random_element(elements=available_pids)
#             uid = fake.random_element(elements=uids)
#             key = (uid,pid)
#             # if i == 230:
#             #     print("start debugging")
#             # while key in already_done_keys:
#             #     pid = fake.random_element(elements=available_pids)
#             #     uid = fake.random_element(elements=uids)
#             rating = fake.random_int(min=1, max=5)
#             review = fake.sentence(nb_words=10)
#             time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
#             writer.writerow([uid, pid, rating,review,time])
#             # already_done_keys.append(key)
#         print(f'{num_product_ratings} generated')
#     return

# def gen_seller_ratings(num_seller_ratings, s_uids, uids):
#     already_done_keys = [[]]
#     with open(file_path + 'SellerRatings.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Seller Ratings...', end=' ', flush=True)
#         for i in range(num_seller_ratings):
#             if i % 10 == 0:
#                 print(f'{i}', end=' ', flush=True)
#             s_uid = fake.random_element(elements=s_uids)
#             uid = fake.random_element(elements=uids)
#             key = (uid,s_uid)
#             while key in already_done_keys:
#                 s_uid = fake.random_element(elements=s_uids)
#                 uid = fake.random_element(elements=uids)
#             rating = fake.random_int(min=1, max=5)
#             review = fake.sentence(nb_words=10)
#             time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
#             writer.writerow([uid, s_uid, rating,review,time])
#             already_done_keys.append(key)
#         print(f'{num_seller_ratings} generated')
#     return

def gen_products(num_products, ratings_prods):
    pid = -1
    available_pids = []
    names = []
    print(ratings_prods)
    
    with open(file_path + 'Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        with open("../outside_data/" + 'products_sample.csv', 'r') as r:
            reader = get_csv_reader(r)
            for row in reader:
                pid+=1
                if pid > 0:
                    if pid %10 ==0:
                        print(f'{pid}', end=' ', flush=True)
                    if pid > num_products:
                        break
                    pname = row[3]
                    if pname in names:
                        pid-=1
                        continue
                    # price = row[6]
                    if row[6] != '':
                        price = int(row[6])/81
                    else:
                        price = 400/81
                    available = fake.random_element(elements=('true', 'true', 'true', 'true', 'false'))
                    if str(pid-1) in ratings_prods:
                        rating_array = ratings_prods[str(pid-1)]
                        sum = 0
                        for i in rating_array:
                            sum+=i
                        rating = sum/len(rating_array)
                    else:
                        rating = 0
                    descriptions = row[10]
                    category = row[4].split(">>")[0][2:].split("\"]")[0]
                    if len(category)>39:
                        category = "Other"
                    images = row[8].split("\"\"")[0][2:].replace('\"','').split(",")[0]
                    if len(images) != 0 and images[-1] == ']':
                        images = images[:-1]
                    if available == 'true':
                        available_pids.append(pid-1)
                    writer.writerow([pid-1, pname, category, descriptions, images, price, rating, available])
                    names.append(pname)
                    # if "Kennel Rubber Dumbell" in pname:
                    # print(rating, end = ' ')
    return available_pids

def gen_ratings(num_ratings):
    already_done_keys = []
    transactions = []
    ratings_prods = {}
    with open(file_path + 'Transactions.csv', 'r') as r:
        reader = get_csv_reader(r)
        for row in reader:
            transactions.append(row)
            
    # with open("../outside_data/" + 'fake_reviews.csv', 'r') as r:
    #     reader = get_csv_reader(r)
    #     reader = list(reader)
    #     review = reader[fake.random_int(min=1, max=20000)][3]
    #     print(review)
    with open(file_path + 'Ratings.csv', 'w') as f:
        with open("../outside_data/" + 'fake_reviews.csv', 'r') as r:
            reader = get_csv_reader(r)
            reader = list(reader)
            writer = get_csv_writer(f)
            print('Ratings...', end=' ', flush=True)
            for i in range(num_ratings):
                if i % 5 == 0:
                    print(f'{i}', end=' ', flush=True)
                transaction = fake.random_element(elements=transactions)
                while transaction in already_done_keys:
                    transaction = fake.random_element(elements=transactions)
                uid = transaction[0]
                sid = transaction[1]
                pid = transaction[2]
                rand_int = fake.random_int(min=1, max=20000)
                rating = int(float(reader[rand_int][1]))
                review = reader[rand_int][3]
                time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
                writer.writerow([uid, sid, pid, rating,review,time])
                already_done_keys.append(transaction)
                if pid in ratings_prods:
                    ratings_prods[pid].append(rating)
                else:
                    ratings_prods[pid]= [rating]
            print(f'{num_ratings} generated')
    # print(ratings_prods)
    gen_products(num_products,ratings_prods)
    return

if __name__ == "__main__":
    # uids = gen_users(num_users)
    available_pids = gen_products(num_products,{})
    s_uids, uids = gen_sellers(num_sellers)
    gen_carts(num_cart_items, uids, s_uids, available_pids)
    gen_transactions(num_purchases, available_pids, uids,s_uids)
    # #gen_prod_ratings(num_product_ratings, available_pids, uids)
    # #gen_seller_ratings(num_seller_ratings, s_uids, uids)
    gen_forsales(num_forsale_items, s_uids, available_pids)
    gen_ratings(num_ratings)
