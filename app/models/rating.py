from pickletools import read_stringnl_noescape
from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request


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
ORDER BY time_reviewed DESC
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


    @staticmethod
    def get_recent_pid(pid, k):
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
WHERE pid = :pid
ORDER BY time_reviewed DESC
''',
                              pid=pid)
        return [Rating(*row) for row in rows[:k]]
    
    @staticmethod
    def get_recent_uid(uid, k):
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
WHERE uid = :uid
ORDER BY time_reviewed DESC
''',
                              uid=uid)
        return [Rating(*row) for row in rows[:k]]


    @staticmethod
    def get_prod_reviews(pid): 
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
WHERE pid = :pid
''',
                                pid = pid)
        return [Rating(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
''')
        return [Rating(*row) for row in rows]
    
    @staticmethod
    def get_specific_review(uid, pid):
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed
FROM Ratings
WHERE pid = :pid AND uid =:uid
ORDER BY time_reviewed DESC
''',
                              pid=pid,uid=uid)
        return [Rating(*row) for row in rows]
    
    @staticmethod
    def updateReview(uid, pid,reviewvalue,ratingvalue):
        rows = app.db.execute("""
UPDATE Ratings
SET review = :reviewvalue, rating=:ratingvalue
WHERE uid = :uid and pid = :pid
""",
                              uid=uid, pid=pid,ratingvalue=ratingvalue,reviewvalue=reviewvalue)
        # return [Rating(*row) for row in rows]

    
