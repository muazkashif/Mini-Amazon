from flask import current_app as app


class Product:
    def __init__(self, id, name, description, rating,images, price, available, category):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.rating = rating
        self.description = description
        self.category = category
        self.images = images

    @staticmethod
    def get_top_k_products(k):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                            k = k)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_name(id):
        name = app.db.execute('''
SELECT name
FROM Products
WHERE id = :id
''',
                            id = id)
        return name


    @staticmethod
    def get_price(id):
        name = app.db.execute('''
SELECT price
FROM Products
WHERE id = :id
''',
                            id = id)
        return name


    @staticmethod
    def sort_ratings_desc():
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, price, available, category
FROM Products
ORDER BY rating DESC
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def sort_ratings_asc():
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, price, available, category
FROM Products
ORDER BY rating ASC
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def sort_price_desc():
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, price, available, category
FROM Products
ORDER BY price DESC
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def sort_price_asc():
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, price, available, category
FROM Products
ORDER BY price ASC
''')
        return [Product(*row) for row in rows]


    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating,images, price, available, category
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, images, price, available, category
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_prod_category(cat):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, price, available, category
FROM Products
WHERE category = :cat
''',
                              cat=cat)
        return [Product(*row) for row in rows]
