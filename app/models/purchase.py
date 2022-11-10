from flask import current_app as app


class Purchase:
    def __init__(self, uid, sid, pid, quantity, time_purchased, order_status):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.time_purchased = time_purchased
        self.order_status = order_status

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