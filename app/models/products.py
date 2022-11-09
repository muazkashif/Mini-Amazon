from flask import current_app as app


class Product:
    def __init__(self, id, name, description, rating, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.rating = rating
        self.description = description

    @staticmethod
    def get_top_k_products(k):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                            k= k)
        return [Product(*row) for row in rows]



    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, descriptions, rating, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]