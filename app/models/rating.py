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
    def get_user_ratings(uid):
        rows = app.db.execute('''
SELECT uid, sid, pid, Ratings.rating, review, time_reviewed, name
FROM Ratings JOIN Products ON Ratings.pid=Products.id
WHERE uid = :uid
ORDER BY time_reviewed DESC
''',
                              uid=uid)
        return rows

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
ORDER BY time_reviewed DESC
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
    def updateReview(uid, pid,reviewvalue,ratingvalue,time):
        rows = app.db.execute("""
UPDATE Ratings
SET review = :reviewvalue, rating=:ratingvalue, time_reviewed=:time
WHERE uid = :uid and pid = :pid
""",
                              uid=uid, pid=pid,ratingvalue=ratingvalue,reviewvalue=reviewvalue,time=time)
        # return [Rating(*row) for row in rows]
        
    @staticmethod
    def addReview(uid, sid, pid,reviewvalue,ratingvalue,time):
        rows = app.db.execute("""
INSERT INTO Ratings(uid, sid, pid, rating,review,time_reviewed)
VALUES(:uid, :sid, :pid, :ratingvalue, :reviewvalue, :time)
RETURNING uid
""",
                              uid=uid, sid=sid, pid=pid,ratingvalue=ratingvalue,reviewvalue=reviewvalue,time=time)
        # return [Rating(*row) for row in rows]
        
    @staticmethod
    def get_ratings_for_avg(pid):
        rows = app.db.execute('''
SELECT AVG(rating) AS avrg
FROM Ratings
WHERE pid = :pid
''',
                              pid=pid)
        avg = rows[0][0]
        return avg
    
    @staticmethod
    def get_number_of_ratings(pid):
        rows = app.db.execute('''
SELECT COUNT(rating) AS cnt
FROM Ratings
WHERE pid = :pid
''',
                              pid=pid)
        cnt = rows[0][0]
        return cnt

    @staticmethod
    def get_seller_ratings(sid):
        rows = app.db.execute('''
SELECT *
FROM Ratings, Products
WHERE sid = :sid AND pid = id
ORDER BY time_reviewed DESC
''',
                              sid=sid)
        return rows if rows else None
    
    @staticmethod
    def delete_review(uid,pid):
        rows = app.db.execute('''
DELETE FROM Ratings
WHERE uid = :uid and pid = :pid
''',
                              uid=uid,pid=pid)
        return

    @staticmethod
    def get_ratings_seller_avg(sid):
        rows = app.db.execute('''
SELECT AVG(rating) AS avrg
FROM Ratings
WHERE sid = :sid
''',
                              sid = sid)
        avg = rows[0][0]
        return avg if rows else None
    
