from tkinter.simpledialog import SimpleDialog
from flask import current_app as app


class Seller:
    def __init__(self, pid, sid, quantity):
        self.pid = pid
        self.sid = sid
        self.quantity = quantity


    @staticmethod
    def get_inventory_by_sid(sid):
        rows = app.db.execute('''
SELECT pid, sid, quantity
FROM ForSaleItems
WHERE sid = :sid
''',
                              sid=sid)
        return [Seller(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT pid, sid, quantity
FROM ForSaleItems
''')
        return [Seller(*row) for row in rows]