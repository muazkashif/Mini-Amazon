from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.rating import Rating
from .models.purchase import Purchase
from datetime import datetime
from decimal import Decimal
from .models.seller import Seller
from .models.transactions import Transaction


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_product_page.index', k = 1))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main_product_page.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_product_page.index', k = 1))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data, 
                         form.address.data,
                         0,
                         datetime.today().strftime('%Y-%m-%d')):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.opener_page'))

@bp.route('/user_profile', methods = ['GET', 'POST'])
@bp.route('/user_profile/',methods = ['GET', 'POST'])
def user_profile():
    if current_user.is_authenticated:
        sellers = Seller.get_sellers()
        check = False
        if current_user.id in sellers: ##Issue with checking membership
            check = True
        user_info = User.get(current_user.id)
        purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('user_profile.html',
                            info=user_info, purchase_history=purchases, purchase_history_len=len(purchases), logged_in=True, sell = check)
    return render_template('main_product_page.html')

@bp.route('/update_Balance', methods = ['POST'])
def update_balance():
    toAdd = request.form.get('addBalance')
    if (User.is_float(toAdd) == False or Decimal(toAdd) < 0):
        flash('Invalid value. Please enter a valid positive integer or decimal.')
        return redirect(url_for('users.user_profile'))
    else:
        value = User.get(current_user.id).balance + Decimal(request.form.get('addBalance'))
        User.updateBalance(current_user.id, value)
        return redirect(url_for('users.user_profile'))

@bp.route('/user_update_form', methods = ['GET', 'POST'])
def user_form():
    return render_template('user_update_form.html')

@bp.route('/update_user_info', methods = ['GET', 'POST'])
def update_info():
    email = request.form.get('new_email')
    print(email)
    password = request.form.get('new_password')
    firstname = request.form.get('new_firstname')
    lastname = request.form.get('new_lastname')
    address = request.form.get('new_address')
    if (email == None or User.email_exists(email) or password == None or firstname == None or lastname == None or address == None):
        flash('INVALID INPUTS!')
        return redirect(url_for('users.user_form'))
    else:
        User.updateUser(current_user.id, email, password, firstname, lastname, address)
        return redirect(url_for('users.user_profile'))

@bp.route('/add_seller', methods = ['POST', 'GET'])
def add_seller():
    Seller.add_seller_relation(current_user.id)
    return redirect(url_for('users.user_profile'))


@bp.route('/seller_page', methods = ['POST', 'GET'])
def see_seller_page():
    no_ratings = False
    user_info = User.get(current_user.id)
    transactions = Transaction.get_transactions(current_user.id)
    if transactions is None:
        total = 0
    else:
        total = len(transactions)
    status_count = Transaction.count_status(current_user.id)
    all_counts = [["Delivered", 0], ["Processing", 0], ["Received", 0], ["Shipped", 0]]
    if status_count is not None:
        for i in range(len(status_count)):
            for j in range(4): 
                if status_count[i][0] == all_counts[j][0]:
                    all_counts[j][1] = status_count[i][1]
    seller_ratings = Rating.get_seller_ratings(current_user.id)
    if seller_ratings is None:
        rating_count = 0
        seller_rating = "N/A"
        no_ratings = True; 
    else:
        rating_count = len(seller_ratings)
        seller_rating = round(Rating.get_ratings_seller_avg(current_user.id), 2)

    return render_template('seller_pers_page.html', info = user_info, length = total, counts = all_counts, num_ratings = rating_count, seller_rating = seller_rating,
    seller_ratings = seller_ratings, no_ratings = no_ratings)

@bp.route('/seller_transaction', methods = ['POST', 'GET'])
def see_seller_transactions():
    check = False
    transactions = Transaction.get_transactions(current_user.id)
    if transactions is None:
        check = True
    return render_template('seller_transactions.html',prod = transactions, empty = check)

@bp.route('/seller_products', methods = ['POST', 'GET'])
def see_seller_products():
    check = False
    pers_products = Transaction.seller_prod(current_user.id)
    if pers_products is None:
        check = True
    return render_template('seller_products.html', prod = pers_products, empty = check, )

@bp.route('/withdraw', methods = ['POST'])
def withdraw():
    toWithdraw = request.form.get('withdrawBalance')
    balance = User.get(current_user.id).balance
    if (User.is_float(toWithdraw) == False or Decimal(toWithdraw) < 0 or Decimal(toWithdraw) > balance):
        flash('Invalid value. Please enter a valid positive integer or decimal that is less than current balance.')
        return redirect(url_for('users.user_profile'))
    else:
        newBalance = balance - Decimal(toWithdraw)
        flash('$' + str(toWithdraw) + ' are being transferred to your connected bank account.')
        User.updateBalance(current_user.id, newBalance)
        return redirect(url_for('users.user_profile'))

@bp.route('/view_order/<uid>break<time_purchased>', methods = ['GET', 'POST'])
def view_order(uid,time_purchased):
    purchases = Purchase.get_order(uid, time_purchased)
    return render_template('orders.html',
                            purchases=purchases, purchases_len=len(purchases))