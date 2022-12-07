from flask import current_app as app
from datetime import datetime

class Purchase:
    def __init__(self, uid, sid, pid, quantity, price, time_purchased, order_status, rating, review, time_updated):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.price = price
        self.time_purchased = time_purchased
        self.order_status = order_status
        self.rating = rating
        self.review = review
        self.time_updated = time_updated


    @staticmethod
    def remove(uid, pid, sid):
        try:
            query_string = "DELETE FROM Transactions WHERE uid = " + str(uid) + "and pid = " + str(pid) + "and sid = " + str(sid)
            app.db.execute(query_string,
                                  uid=uid, pid=pid, sid=sid)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def add(uid, pid, sid, quantity, price, time_purchased):
        try:
            app.db.execute("""
INSERT INTO Transactions(uid, pid, sid, quantity, price, time_purchased, order_status, time_updated)
VALUES(:uid, :pid, :sid, :quantity, :price, :time_purchased, :order_status, :time_purchased)
RETURNING uid
""",
                                  uid=uid, pid=pid, sid=sid, quantity=quantity, price=price, time_purchased=time_purchased, order_status="Processing")
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Transactions
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, price, time_purchased, order_status, NULL, NULL, time_updated
FROM Transactions
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_purchases_by_uid(uid):
        rows = app.db.execute(
'''SELECT *
FROM Products P, (SELECT T.uid, T.sid, T.pid, T.quantity, T.price, T.time_purchased, T.order_status, R.rating, R.review, T.time_updated
FROM Transactions T LEFT JOIN 
(SELECT uid, sid, pid, rating, review
FROM Ratings
WHERE uid=:uid) R ON T.pid=R.pid AND T.sid = R.sid
WHERE T.uid = :uid
ORDER BY T.time_purchased DESC) PUR
WHERE P.id = PUR.pid
''',
                              uid=uid)
        print(rows)
        return rows

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, price, time_purchased, order_status, NULL, NULL, time_updated
FROM Transactions
ORDER BY time_purchased DESC
''')
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_order(uid, time_purchased):
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, price, time_purchased, order_status, NULL, NULL, time_updated
FROM Transactions
WHERE uid = :uid AND time_purchased = :time_purchased
ORDER BY time_purchased DESC
''', 
                        uid=uid, time_purchased=time_purchased)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_quantity_purchased(uid,pid):
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, price, time_purchased, order_status, NULL, NULL, time_updated
FROM Transactions
WHERE uid = :uid and pid=:pid
''',
                            uid=uid,pid=pid)
        return [Purchase(*row) for row in rows]