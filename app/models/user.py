from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

from .. import login


class User(UserMixin):
    def __init__(self, id, email, password, firstname, lastname, address, balance, date):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.address = address
        self.balance = balance
        self.date = date


    @staticmethod
    def get_balance(id):
        rows = app.db.execute('''
SELECT balance
FROM Users 
WHERE id = :id
''',
                              id=id)
        return rows[0][0]

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT id, email, password, firstname, lastname, address, balance, date
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][2], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0])) if rows else None

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def is_float(element: any) -> bool:
    #If you expect None to be passed:
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def register(email, password, firstname, lastname, address, balance, date):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, balance, date)
VALUES(:email, :password, :firstname, :lastname, :address, :balance, :date)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address=address,
                                  balance=balance, date=date)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, password, firstname, lastname, address, balance, date
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
    
    @staticmethod
    def updateBalance(id, value):
        rows = app.db.execute("""
UPDATE Users
SET balance = :value
WHERE id = :id
""",
                              id=id, value=value)
        #return User(*(rows[0])) if rows else None

    @staticmethod
    def updateUser(id, email, password, firstname, lastname, address):
        rows = app.db.execute("""
UPDATE Users
SET email = :email, password = :password, firstname = :firstname, lastname = :lastname, address = :address
WHERE id = :id
""",
                              id=id, email=email, password=generate_password_hash(password), firstname=firstname, lastname=lastname, address=address)
        return None
