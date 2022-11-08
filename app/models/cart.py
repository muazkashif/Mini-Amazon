from flask import current_app as app
from .user import User


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
    def get_all():
        rows = app.db.execute('''
SELECT uid, pid, sid, quantity
FROM Carts
''')
        return [Cart(*row) for row in rows]

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