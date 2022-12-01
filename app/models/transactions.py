from flask import current_app as app


class Transaction:
    def __init__(self, uid, sid, pid, quantity, time_purchased, order_status):
        self.uid = pid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.time_purchased = time_purchased
        self.order_status = order_status



    @staticmethod
    def get_transactions(id):
        rows = app.db.execute('''
SELECT uid, sid, pid, quantity, time_purchased, order_status
FROM Transactions
WHERE sid = :id
ORDER BY time_purchased DESC
''',                                    id = id)
        return [Transaction(*row) for row in rows]
    
    @staticmethod
    def getSeller(pid,uid):
        rows = app.db.execute('''
SELECT sid
FROM Transactions
WHERE pid = :pid AND uid = :uid
''',                                    pid = pid, uid=uid)
        return rows[0][0]