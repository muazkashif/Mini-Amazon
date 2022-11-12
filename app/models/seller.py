# from tkinter.simpledialog import SimpleDialog
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

    @staticmethod
    def add_seller_relation(id):
        try:
            app.db.execute("""
INSERT INTO Sellers(id)
VALUES(:id)
RETURNING id
""",
                                  id=id)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
