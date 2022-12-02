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