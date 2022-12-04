from flask import current_app as app


class Product:
    def __init__(self,  id, name, descriptions, rating, images, available, category):
        self.id = id
        self.name = name
        self.category = category
        self.description = descriptions
        self.images = images
        self.rating = rating
        self.available = available

    @staticmethod
    def get_top_k_products(k):
        rows = app.db.execute('''
SELECT id, name, available
FROM Products JOIN 
ORDER BY price DESC
LIMIT :k
''',
                            k = k)
        return [Product(*row) for row in rows]

    @staticmethod
    def update_product(pid, name, description, category, images, rating, available):
        rows = app.db.execute('''
UPDATE Products
SET id = :pid, name = :name, descriptions = :description, category = :category, images = :images, rating = :rating, available = :available
WHERE id = :pid
''',
                            pid = pid, name = name, description = description, category = category, images = images, rating = rating, available = available)
        return

    @staticmethod
    def get_name(id):
        name = app.db.execute('''
SELECT name
FROM Products
WHERE id = :id
''',
                            id = id)
        return name


#     @staticmethod
#     def get_price(id):
#         name = app.db.execute('''
# SELECT price
# FROM Products
# WHERE id = :id
# ''',
#                             id = id)
#         return name

    @staticmethod
    def delete_product_seller(id, sid):
        name = app.db.execute('''
DELETE
FROM ForSaleItems
WHERE pid = :id AND sid = :sid
''',
                            id = id, sid = sid)
        return


    @staticmethod
    def sort_ratings_desc():
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, available, category
FROM Products
ORDER BY rating DESC
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def add_new_product(name, description, category, rating, images, available):
        try:
            rows = app.db.execute("""
INSERT INTO Products(name, category, descriptions, images, rating, available)
VALUES(:name, :category, :description, :images, :rating, :available)
RETURNING id
""",
                    name = name, description = description, category = category, rating = rating, images = images, available = available)
            id = rows[0][0]
            return id
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


    @staticmethod
    def sort_ratings_asc():
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, available, category
FROM Products
ORDER BY rating ASC
''')
        return [Product(*row) for row in rows]

#     @staticmethod
#     def sort_price_desc():
#         rows = app.db.execute('''
# SELECT id, name, descriptions, rating, images, available, category
# FROM Products
# ORDER BY price DESC
# ''')
#         return [Product(*row) for row in rows]

#     @staticmethod
#     def sort_price_asc():
#         rows = app.db.execute('''
# SELECT id, name, descriptions, rating, price, available, category
# FROM Products
# ORDER BY price ASC
# ''')
#         return [Product(*row) for row in rows]


    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, available, category
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available = True):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, available, category
FROM Products
ORDER BY name
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_offset(available, k, order_prop,order_by):
        # if order_prop == "price":
        #     print("in price")
        #     if order_by == "ASC":
        #         rows = app.db.execute('''
        # SELECT id, name, descriptions, rating, images, available, category
        # FROM Products
        # WHERE available = :available
        # ORDER BY price ASC
        # LIMIT 20
        # OFFSET :k 
        # ''',
        #                             available=available, k=k)
        #     elif order_by == "DESC":
        #         rows = app.db.execute('''
        # SELECT id, name, descriptions, rating, images, available, category
        # FROM Products
        # WHERE available = :available
        # ORDER BY price DESC
        # LIMIT 20
        # OFFSET :k 
        # ''',
        #                             available=available, k=k)
        if order_prop == "rate":
            if order_by == "ASC":
                rows = app.db.execute('''
        SELECT id, name, descriptions, rating, images, available, category
        FROM Products
        WHERE available = :available
        ORDER BY rating ASC
        LIMIT 20
        OFFSET :k 
        ''',
                                    available=available, k=k)
            if order_by == "DESC":
                rows = app.db.execute('''
        SELECT id, name, descriptions, rating, images, available, category
        FROM Products
        WHERE available = :available
        ORDER BY rating DESC
        LIMIT 20
        OFFSET :k 
        ''',
                                    available=available, k=k)
        else:
            rows = app.db.execute('''
        SELECT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
        FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
        WHERE available = :available AND Products.id = S.pid
        LIMIT 20
        OFFSET :k 
        ''',
                                    available=available, k=k)
        return rows

    @staticmethod
    def get_prod_category(cat):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, available, category
FROM Products
WHERE category = :cat
''',
                              cat=cat)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_search(search):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, available, category
FROM Products
WHERE name LIKE concat('%',:search,'%') OR descriptions LIKE concat('%',:search,'%')
ORDER BY name
''',
                              search = search)
        return [Product(*row) for row in rows] if rows else None
    
    @staticmethod
    def update_rating(pid,avg):
        rows = app.db.execute('''
UPDATE Products
SET rating=:avg
WHERE id = :pid
''',
                              pid=pid,avg=avg)
        # return [Product(*row) for row in rows]
    
  