from flask import current_app as app
from datetime import datetime

class Purchase:
    def __init__(self, uid, sid, pid, quantity, time_purchased, order_status):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.time_purchased = time_purchased
        self.order_status = order_status


    @staticmethod
    def remove(uid, pid):
        try:
            query_string = "DELETE FROM Transactions WHERE uid = " + str(uid) + "and pid = " + str(pid)
            app.db.execute(query_string,
                                  uid=uid, pid=pid)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def add(uid, pid, sid, quantity):
        try:
            app.db.execute("""
INSERT INTO Transactions(uid, pid, sid, quantity, time_purchased, order_status)
VALUES(:uid, :pid, :sid, :quantity, :time_purchased, :order_status)
RETURNING uid
""",
                                  uid=uid, pid=pid, sid=sid, quantity=quantity, time_purchased=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), order_status="no")
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
SELECT uid, sid, pid, quantity, time_purchased, order_status
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
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, time_purchased, order_status
FROM Transactions
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, time_purchased, order_status
FROM Transactions
ORDER BY time_purchased DESC
''')
        return [Purchase(*row) for row in rows]