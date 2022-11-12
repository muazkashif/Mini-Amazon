from flask_login import current_user
import datetime
from decimal import Decimal
from flask import render_template, redirect, url_for, flash, request
from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.rating import Rating

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
    return render_template('edit_review_page.html',
                          ratings=ratings)
    
@bp.route('/update_review/<uid>break<pid>', methods = ['GET', 'POST'])
def update_review(uid,pid):
    reviewvalue = request.form.get('reviewText')
    ratingvalue = Decimal(request.form.get('ratingText'))
    Rating.updateReview(uid,pid,reviewvalue,ratingvalue)
    return redirect(url_for('users.user_profile'))

@bp.route('/view_all_reviews/<uid>', methods = ['GET', 'POST'])
def view_all(uid):
    ratings = Rating.get(uid)
    return render_template('all_review_page.html',
                          ratings=ratings, ratings_len=len(ratings))