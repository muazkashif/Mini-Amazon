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


    @staticmethod
    def get_quantity(pid, sid):
        query_string = "SELECT quantity FROM ForSaleItems WHERE pid = " + str(pid) + " and sid = " + str(sid)
        rows = app.db.execute(query_string,
                              pid=pid, sid=sid)
        return rows


    @staticmethod
    def add(pid, sid, quantity):
        try:
            app.db.execute("""
INSERT INTO ForSaleItems(pid, sid, quantity)
VALUES(:pid, :sid, :quantity)
""",
                                  pid=pid, sid=sid, quantity=quantity)
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def remove(pid, sid, quantity):
        try:
            query_string = "DELETE FROM ForSaleItems WHERE pid = " + str(pid) + "and sid = " + str(sid) + "and quantity = " + str(quantity)
            app.db.execute(query_string,
                                  pid=pid, sid=sid, quantity=quantity)
            return None
        except Exception as e:
            print(str(e))
            return None