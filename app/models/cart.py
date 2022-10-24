from flask import current_app as app


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
        return Cart(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, pid, sid, quantity
FROM Carts
''')
        return [Cart(*row) for row in rows]
