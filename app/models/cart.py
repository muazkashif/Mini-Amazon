from flask import current_app as app
from .user import User

from sqlalchemy import select, update, delete, values


class Cart:
    def __init__(self, uid, pid, sid, quantity):
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.quantity = quantity

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, pid, sid, quantity
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_pid_category(uid):
        rows = app.db.execute('''
SELECT uid, category
FROM Carts, Products
WHERE pid = id and uid = :uid
''',
                              uid = uid)
        return rows

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, pid, sid, quantity
FROM Carts
''')
        return [Cart(*row) for row in rows]

    @staticmethod
    def remove(uid, pid):
        try:
            query_string = "DELETE FROM Carts WHERE uid = " + str(uid) + "and pid = " + str(pid)
            app.db.execute(query_string,
                                  uid=uid, pid=pid)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def delete_product_cart(uid, pid, sid):
        name = app.db.execute('''
DELETE
FROM Carts
WHERE pid = :pid AND uid = :uid AND sid = :sid
''',
                            pid = pid, uid = uid, sid = sid)
        return

    @staticmethod
    def remove(uid, pid, sid):
        try:
            query_string = "DELETE FROM Carts WHERE uid = " + str(uid) + "and pid = " + str(pid) + "and sid = " + str(sid)
            app.db.execute(query_string,
                                  uid=uid, pid=pid, sid=sid)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def clear(uid):
        try:
            query_string = "DELETE FROM Carts WHERE uid = " + str(uid)
            app.db.execute(query_string,
                                  uid=uid)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


    @staticmethod
    def add(uid, pid, sid, quantity):
        try:
            rows = app.db.execute("""
INSERT INTO Carts(uid, pid, sid, quantity)
VALUES(:uid, :pid, :sid, :quantity)
RETURNING uid
""",
                                  uid=uid, pid=pid, sid=sid, quantity=quantity)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None