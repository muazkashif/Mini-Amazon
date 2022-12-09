from flask import current_app as app


class Coupons:
    def __init__(self, code, pid, category, effect):
        self.code = code
        self.pid = pid
        self.category = category
        self.effect = effect


    @staticmethod
    def get_effect(code):
        rows = app.db.execute('''
SELECT *
FROM Coupons
WHERE code = :code
''',            code = code)
        return rows if rows else None