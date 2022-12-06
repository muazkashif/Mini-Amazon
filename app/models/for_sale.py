from flask import current_app as app


class ForSaleItems:
    def __init__(self, pid, sid, quantity, price):
        self.pid = pid
        self.sid = sid
        self.quantity = quantity
        self.price = price



    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT *
FROM ForSaleItems
''')
        return [ForSaleItems(*row) for row in rows]

    @staticmethod
    def update_sale(pid, sid, price, quantity):
        rows = app.db.execute('''
UPDATE ForSaleItems
SET pid = :pid, sid = :sid, price = :price, quantity = :quantity
WHERE pid = :pid and sid = :sid
''',
                        pid = pid, sid = sid, price = price, quantity = quantity)
        return 

    @staticmethod
    def get_all_products_for_sale():
        rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id
''')
        return rows


    @staticmethod
    def get_all_products_for_sale_fil_price(price):
        rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id AND avg <= :price
''',
                                   price = price)
        return rows

    @staticmethod
    def get_all_products_for_sale_fil_cat(category):
        rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id AND category = :category
''',
                                    category = category)
        return rows

    @staticmethod
    def get_all_products_for_sale_fil_rate(rating):
        rating1 = int(rating) + 1
        rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id AND rating >= :rating AND rating < :rating1
''',
                                    rating = rating, rating1 = rating1)
        return rows


        

    @staticmethod
    def get_all_products_for_sale_rate(direction):
        if direction == "ASC":
            rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id
ORDER BY rating 
''')
        else:
            rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id
ORDER BY rating DESC
''')
        return rows

    @staticmethod
    def get_all_products_for_sale_price(direction):
        if direction == "ASC":
            rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id
ORDER BY avg 
''')
        else:
            rows = app.db.execute('''
SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
WHERE S.pid = Products.id
ORDER BY avg DESC
''')
        return rows

    @staticmethod
    def get_all_products_for_sale_search(search):
        rows = app.db.execute('''
        SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
        FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
        WHERE Products.id = S.pid AND (name LIKE concat('%',:search,'%') OR descriptions LIKE concat('%',:search,'%'))
        ''',
                        search = search)
        
        # '''
        # SELECT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
        # FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
        # WHERE available = :available AND Products.id = S.pid
        # LIMIT 20
        # OFFSET :k 
        # '''
        
        # '''
        # SELECT DISTINCT id, name, descriptions, rating, images, available, category, ROUND(avg, 2) as avg
        # FROM Products, (SELECT avg(price) AS avg, pid FROM ForSaleItems GROUP BY pid) as S
        # WHERE Products.id = S.pid AND (name LIKE concat('%',:search,'%') OR descriptions LIKE concat('%',:search,'%'))
        # '''
        return rows if rows else None
        

    @staticmethod
    def get_quantity(pid, sid):
        rows = app.db.execute('''
SELECT * 
FROM ForSaleItems 
WHERE pid = :pid AND sid = :sid
''',
                              pid=pid, sid=sid)
        
        return rows[0][2]

    @staticmethod
    def get_price(pid, sid):
        rows = app.db.execute('''
SELECT price
FROM ForSaleItems 
WHERE pid = :pid AND sid = :sid
''',
                              pid=pid, sid=sid)
        return rows[0]

    @staticmethod
    def add(pid, sid, quantity, price):
        try:
            app.db.execute("""
INSERT INTO ForSaleItems(pid, sid, quantity, price)
VALUES(:pid, :sid, :quantity, :price)
""",
                                  pid=pid, sid=sid, quantity=quantity, price = price)
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def remove(pid, sid, quantity, price):
        try:
            query_string = "DELETE FROM ForSaleItems WHERE pid = " + str(pid) + "and sid = " + str(sid) + "and quantity = " + str(quantity)
            app.db.execute(query_string,
                                  pid=pid, sid=sid, quantity=quantity, price = price)
            return None
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def average_price(pid):
        rows = app.db.execute('''
SELECT avg(price), pid
FROM ForSaleItems
WHERE pid = :pid
''',
                              pid=pid)
        return [ForSaleItems(*row) for row in rows]

    @staticmethod
    def get_sellers_for_product(pid):
        rows = app.db.execute("""
SELECT *
FROM ForSaleItems
WHERE pid = :pid
""", 
                                    pid = pid)
        return [ForSaleItems(*row) for row in rows]

    @staticmethod
    def get_prod_seller_info(pid, sid):
        rows = app.db.execute("""
SELECT *
FROM ForSaleItems
WHERE pid = :pid AND sid = :sid
""", 
                                    pid = pid, sid = sid)
        return [ForSaleItems(*row) for row in rows][0]

    @staticmethod
    def add_new_sale(pid, sid, quantity, price):
        try:
            rows = app.db.execute("""
INSERT INTO ForSaleItems(pid, sid, quantity, price)
VALUES(:pid, :sid, :quantity, :price)
""",
                    pid = pid, sid = sid, quantity = quantity, price = price)
            return True
        except Exception as e:
            return None