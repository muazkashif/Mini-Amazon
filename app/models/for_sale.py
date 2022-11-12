from flask import current_app as app


class ForSaleItems:
    def __init__(self, pid, sid, quantity):
        self.pid = pid
        self.sid = sid
        self.quantity = quantity


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT pid, sid, quantity
FROM ForSaleItems
''')
        return [ForSaleItems(*row) for row in rows]