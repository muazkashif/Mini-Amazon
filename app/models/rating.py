from pickletools import read_stringnl_noescape
from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request


class Rating:
    global sort_type
    sort_type = "time_reviewed"
    def __init__(self, uid, sid, pid, rating, review, time_reviewed,votes):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.rating = rating
        self.review = review
        self.time_reviewed = time_reviewed
        self.votes = votes
        
    

    @staticmethod
    def get_user_ratings(uid):
        rows = app.db.execute('''
SELECT uid, sid, pid, Ratings.rating, review, time_reviewed, votes, name
FROM Ratings JOIN Products ON Ratings.pid=Products.id
WHERE uid = :uid
ORDER BY time_reviewed DESC
''',
                              uid=uid,sort=sort_type)
        return rows

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed,votes
FROM Ratings
''')
        return [Rating(*row) for row in rows]


    @staticmethod
    def get_recent_pid(pid, k):
        global sort_type
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed,votes
FROM Ratings
WHERE pid = :pid
ORDER BY time_reviewed DESC
''',
                              pid=pid)
        return [Rating(*row) for row in rows[:k]]
    
    @staticmethod
    def get_recent_uid(uid, k):
        global sort_type
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed,votes
FROM Ratings
WHERE uid = :uid
ORDER BY time_reviewed DESC
''',
                              uid=uid)
        return [Rating(*row) for row in rows[:k]]


    @staticmethod
    def get_prod_reviews(pid): 
        global sort_type
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed,votes
FROM Ratings
WHERE pid = :pid
ORDER BY {} DESC
'''.format(sort_type),
                                pid = pid)
        return [Rating(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, pid, rating, review, time_reviewed,votes
FROM Ratings
''')
        return [Rating(*row) for row in rows]
    
    @staticmethod
    def get_specific_review(uid, pid,sid):
        global sort_type
        rows = app.db.execute('''
SELECT uid, sid, pid, Ratings.rating, review, time_reviewed, votes, name
FROM Ratings, Products
WHERE pid = :pid AND uid =:uid AND sid = :sid and Products.id=Ratings.pid
ORDER BY time_reviewed DESC
''',
                              pid=pid,uid=uid,sid=sid)
        return rows
    
    @staticmethod
    def updateReview(uid, pid,sid,reviewvalue,ratingvalue,time):
        rows = app.db.execute("""
UPDATE Ratings
SET review = :reviewvalue, rating=:ratingvalue, time_reviewed=:time
WHERE uid = :uid and pid = :pid and sid = :sid
""",
                              uid=uid, pid=pid,ratingvalue=ratingvalue,reviewvalue=reviewvalue,time=time,sid=sid)
        # return [Rating(*row) for row in rows]
        
    @staticmethod
    def addReview(uid, sid, pid,reviewvalue,ratingvalue,time):
        rows = app.db.execute("""
INSERT INTO Ratings(uid, sid, pid, rating,review,time_reviewed,votes)
VALUES(:uid, :sid, :pid, :ratingvalue, :reviewvalue, :time,0)
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
        global sort_type
        rows = app.db.execute('''
SELECT *, Ratings.rating as rate
FROM Ratings, Products
WHERE sid = :sid AND pid = id
ORDER BY time_reviewed DESC
''',
                              sid=sid)
        return rows if rows else None
    
    @staticmethod
    def delete_review(uid,pid,sid):
        rows = app.db.execute('''
DELETE FROM Ratings
WHERE uid = :uid and pid = :pid and sid = :sid
''',
                              uid=uid,pid=pid, sid=sid)
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
    
    @staticmethod
    def getvotes_for_Review(uid,pid,sid):
        rows = app.db.execute('''
SELECT votes
FROM Ratings
WHERE uid = :uid and pid = :pid and sid = :sid
''',
                              sid = sid,uid=uid,pid=pid)
        return rows[0][0]
        
    @staticmethod
    def change_upvote_Review(uid,pid,sid,val):
        rows = app.db.execute('''
UPDATE Ratings
SET votes = :val
WHERE uid = :uid and pid = :pid and sid = :sid
''',
                              sid = sid,uid=uid,pid=pid,val=val)
        return
    
    @staticmethod
    def change_order_by(type):
        global sort_type
        sort_type = type
        return
    
    @staticmethod
    def get_rating_sort():
        global sort_type
        return sort_type
    

   
