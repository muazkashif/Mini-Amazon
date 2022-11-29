from flask_login import current_user
import datetime
from decimal import Decimal
from flask import render_template, redirect, url_for, flash, request
from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.rating import Rating
from datetime import datetime

from flask import Blueprint
bp = Blueprint('product_rating_view', __name__)


@bp.route('/product_reviews/')
def index():
    # get all available products for sale:
    ratings = Rating.get_all()
    return render_template('rating_view.html',
                           ratings=ratings)

@bp.route('/product_reviews/<pid>')
def show_rating_uid(pid):
    ratings = Rating.get_recent_pid(pid, k=5)
    return render_template('product_rating_view.html',
                           ratings=ratings)
    
@bp.route('/write_review/<uid>break<pid>', methods = ['GET', 'POST'])
def write_review(uid,pid):
    ratings = Rating.get_specific_review(uid,pid)
    if (len(ratings)>0):
        return render_template('edit_review_page.html',
                            ratings=ratings,user=uid,product=pid)
    else:
        return render_template('add_review_page.html',
                            ratings=ratings,user=uid,product=pid,sid=2)
    
@bp.route('/update_review/<uid>break<pid>', methods = ['GET', 'POST'])
def update_review(uid,pid):
    reviewvalue = request.form.get('reviewText')
    ratingvalue = Decimal(request.form.get('ratingText'))
    now = datetime.now()
    time = now.strftime("%m-%d-%Y %H:%M:%S")
    Rating.updateReview(uid,pid,reviewvalue,ratingvalue,time)
    return redirect(url_for('ind_prod.show_product', k = pid))

@bp.route('/add_review/<uid>break<pid>break<sid>', methods = ['GET', 'POST'])
def add_review(uid,sid,pid):
    reviewvalue = request.form.get('reviewText')
    ratingvalue = Decimal(request.form.get('ratingText'))
    now = datetime.now()
    time = now.strftime("%m-%d-%Y %H:%M:%S")
    Rating.addReview(uid,sid,pid,reviewvalue,ratingvalue,time)
    return redirect(url_for('ind_prod.show_product', k = pid))

@bp.route('/view_all_reviews/<uid>', methods = ['GET', 'POST'])
def view_all(uid):
    ratings = Rating.get(uid)
    return render_template('all_review_page.html',
                          ratings=ratings, ratings_len=len(ratings))