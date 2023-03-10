from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import datetime

# import sys
# sys.path.insert(0, '/home/aat25/mini-amazon-skeleton/app/models')
# from for_sale import ForSaleItems

num_users = 10000
num_products = 10000
num_purchases = 5000
num_sellers = 2000
num_cart_items = 4000
num_forsale_items = 4000
num_ratings = 5000
num_coupons = 1000



file_path = "../data/"

categories = ["Travel", "Pets", "Kitchenware", "Furniture", "Electronics", "Sports", "Toiletries", "Clothing", "Books", "School"]

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


def gen_carts(num_cart_items, uids, prod_to_seller):
    done = [()]
    with open(file_path + 'Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for i in range(num_cart_items):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            prod_seller = fake.random_element(elements=prod_to_seller)
            while prod_seller == ():
                prod_seller = fake.random_element(elements=prod_to_seller)
            # print(str(prod_seller[0]) + "\n")
            # print(str(prod_seller[1]) + "\n")
            pid = prod_seller[0]
            s_uid = prod_seller[1]
            key = (uid,s_uid,pid)
            while key in done:
                uid = fake.random_element(elements=uids)
                prod_seller = fake.random_element(elements=prod_to_seller)
                pid = prod_seller[0]
                s_uid = prod_seller[1]
                key = (uid,s_uid,pid)
            quantity = fake.random_int(min=1, max=10)
            done.append(key)
            writer.writerow([uid, pid, s_uid, quantity])
        print(f'{num_cart_items} generated')
    return 

def gen_forsales(num_forsale_items, s_uids, available_pids):
    already_done_keys = [()]
    used_pids = []
    with open(file_path + 'ForSaleItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ForSales...', end=' ', flush=True)
        for i in range(num_forsale_items):
            print(f'{i}', end=' ', flush=True)
            pid = fake.random_element(elements=available_pids)
            s_uid = fake.random_element(elements=s_uids)
            key = (pid,s_uid)
            price = round(random.uniform(0, 500), 2)
            while key in already_done_keys:
                pid = fake.random_element(elements=available_pids)
                s_uid = fake.random_element(elements=s_uids)
                key = (pid,s_uid)
            quantity = fake.random_int(min=1, max=10)
            used_pids.append(pid)
            writer.writerow([pid, s_uid, quantity, price])
            already_done_keys.append(key)
        print(f'{num_forsale_items} generated')
    return already_done_keys,used_pids


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


def gen_transactions(num_purchases, uids):
    order_status = ["Received","Processing","Shipped","Delivered"]
    seller_to_prods = []
    already_done = [()]
    
    with open(file_path + 'ForSaleItems.csv', 'r') as r:
        reader = get_csv_reader(r)
        for row in reader:
            seller_to_prods.append(row)
            
            
    with open(file_path + 'Transactions.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=uids)
            s_to_p = fake.random_element(elements=seller_to_prods)
            sid = s_to_p[1]
            pid = s_to_p[0]
            key = (uid,sid,pid)
            while key in already_done:
                uid = fake.random_element(elements=uids)
                s_to_p = fake.random_element(elements=seller_to_prods)
                sid = s_to_p[1]
                pid = s_to_p[0]
                key = (uid,sid,pid)
            quant = fake.random_int(min = 1, max = 5) #CHANGE MAX TO TAKE INTO ACCOUNT STALK
            price = round(random.uniform(0, 500), 2)
            time_purchased = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
            time_updated = time_purchased
            status = fake.random_element(elements = order_status)
            already_done.append(key)
            writer.writerow([uid, sid, pid, quant, price, time_purchased, status, time_updated])
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
    unique = []
    categories_dict = {}
    print(ratings_prods)
    with open("../../outside_data/" + 'Cats_sorted.csv', 'r') as r:
        reader = get_csv_reader(r)
        for row in reader:
            categories_dict[row[0]] = row[1]
    
    with open(file_path + 'Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        with open("../../outside_data/" + 'products_sample.csv', 'r') as r:
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
                    if category in categories_dict:
                        category = categories_dict[category]
                    # category = fake.random_element(elements = ("Travel", "Pets", "Kitchenware", "Furniture", "Electronics", "Sports", "Toiletries", "Clothing", "Books", "School"))
                    # if len(category)>39:
                    #     category = "Other"
                    if category not in categories:
                        categories.append(category)
                    images = row[8].split("\"\"")[0][2:].replace('\"','').split(",")[0]
                    if len(images) != 0 and images[-1] == ']':
                        images = images[:-1]
                    if available == 'true':
                        available_pids.append(pid-1)
                    writer.writerow([pid-1, pname, category, descriptions, images, rating, available])
                    names.append(pname)
                    # if "Kennel Rubber Dumbell" in pname:
                    # print(rating, end = ' ')
                    unique.append(category)
    #print(set(unique))
    return available_pids, categories

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
        with open("../../outside_data/" + 'fake_reviews.csv', 'r') as r:
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
                votes = fake.random_int(min = -3, max = 5)
                rating = int(float(reader[rand_int][1]))
                review = reader[rand_int][3]
                time = fake.date_time_between(start_date = datetime.datetime(2000, 1, 1))
                writer.writerow([uid, sid, pid, rating,review,time,votes])
                already_done_keys.append(transaction)
                if pid in ratings_prods:
                    ratings_prods[pid].append(rating)
                else:
                    ratings_prods[pid]= [rating]
            print(f'{num_ratings} generated')
    # print(ratings_prods)
    gen_products(num_products,ratings_prods)
    return

def gen_coupons(num_coupons, available_pids):
    with open(file_path + 'Coupons.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Coupons...', end=' ', flush=True)
        codes = 1000000000
        for count in range(num_coupons):
            if count % 10 == 0:
                print(f'{count}', end = ' ', flush = True)
            if count % 2 == 0:
                code_use = codes
                codes += 1
                pid = str(fake.random_element(elements = available_pids))
                effect = round(random.uniform(0, .99), 2)
                category = "None"
            else:
                code_use = codes
                codes += 1
                category = fake.random_element(elements = ("Travel", "Pets", "Kitchenware", "Furniture", "Electronics", "Sports", "Toiletries", "Clothing", "Books", "School", "All"))
                effect = round(random.uniform(0, .99), 2)
                pid = "None" 
            writer.writerow([code_use, pid, category, effect])
        print(f'{num_coupons} generated')
    return

def print_cat(cats):
    with open("../../outside_data/" +  'Cats.csv', 'w') as f:
        for i in cats:
            writer = get_csv_writer(f)
            writer.writerow([i])
    return
        

if __name__ == "__main__":
    uids = gen_users(num_users)
    available_pids, categories = gen_products(num_products,{})
    # print("\n\n\n\n\n" + str(len(available_pids)))
    s_uids, uids = gen_sellers(num_sellers)
    prod_to_seller, products_for_sale = gen_forsales(num_forsale_items, s_uids, available_pids)
    #products_for_sale = ForSaleItems.get_pids()
    gen_carts(num_cart_items, uids, prod_to_seller)
    gen_transactions(num_purchases, uids)
    gen_ratings(num_ratings)
    gen_coupons(num_coupons, products_for_sale)
    
    print_cat(categories)
    print("\n")
