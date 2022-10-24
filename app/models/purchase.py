from flask import current_app as app


class Purchase:
    def __init__(self, uid, sid, pid, quant, time_purchased, status):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quant = quant
        self.time_purchased = time_purchased
        self.status = status

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
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
SELECT *
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]
