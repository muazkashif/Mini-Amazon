from flask import current_app as app
from datetime import datetime


class Transaction:
    def __init__(self, uid, sid, pid, quantity, time_purchased, order_status):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.time_purchased = time_purchased
        self.order_status = order_status



    @staticmethod
    def get_transactions(id):
        rows = app.db.execute('''
SELECT *
FROM Transactions, Products, Users
WHERE sid = :id AND Products.id = Transactions.pid AND Transactions.uid = users.id
ORDER BY time_purchased DESC
''',                                    id = id)
        return rows if rows else None
    
    @staticmethod
    def getSellers(uid,pid):
        rows = app.db.execute('''
SELECT DISTINCT sid
FROM Transactions
WHERE pid = :pid AND uid = :uid
''',                                    pid = pid, uid=uid)
        return rows

    @staticmethod
    def update_status(stat, sid, uid, pid, time):

        rows = app.db.execute('''
UPDATE Transactions
SET order_status = :stat
WHERE sid = :sid AND uid = :uid AND pid = :pid AND time_purchased = :time
''',                                    stat = stat, sid = sid, uid = uid, pid = pid, time = time)
        app.db.execute('''
UPDATE Transactions
SET time_updated = :time_updated
WHERE sid = :sid AND uid = :uid AND pid = :pid AND time_purchased = :time
''',                                    stat = stat, sid = sid, uid = uid, pid = pid, time = time, time_updated = datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        return

    @staticmethod
    def seller_prod(id):
        rows = app.db.execute('''
SELECT *
FROM Sellers, (SELECT * FROM ForSaleItems, Products WHERE ForSaleItems.pid = Products.id) AS t
WHERE Sellers.id = :id AND Sellers.id = t.sid
ORDER BY t.name
''',                                    id = id)
        return rows if rows else None

    @staticmethod
    def count_status(id):
        rows = app.db.execute('''
SELECT order_status, count(order_status)
FROM Transactions, Products, Users
WHERE sid = :id AND Products.id = Transactions.pid AND Transactions.uid = users.id
GROUP BY order_status
ORDER BY order_status
''',                                    id = id)
        return rows if rows else None

