from pickletools import read_stringnl_noescape
from flask import current_app as app


class Rating:
    def __init__(self, uid, sid, pid, rating, review, time_reviewed):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.rating = rating
        self.review = review
        self.time_reviewed = time_reviewed

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
WHERE uid = :uid
''',
                              uid=uid)
        return [Rating(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
''')
        return [Rating(*row) for row in rows]
