from flask_login import current_user
import datetime
from decimal import Decimal
from flask import render_template, redirect, url_for, flash, request
from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.rating import Rating
from datetime import datetime
from .models.transactions import Transaction

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
    
@bp.route('/write_review/<uid>_<pid>', methods = ['GET', 'POST'])
def write_review(uid,pid):
    sellers = Transaction.getSellers(uid,pid)
    sids=[]
    for s in sellers:
        sids.append(int(str(s)[1:-2]))
    if len(sellers)==1:
        return redirect(url_for('product_rating_view.review_page', uid = uid, pid=pid, sid=sids[0]))
    else:
        return render_template('choose_seller.html',pid=pid,uid=uid,sellers=sids)

@bp.route('/review_page/<uid>_<pid>_<sid>', methods = ['GET', 'POST'])
def review_page(uid,pid,sid):
    ratings = Rating.get_specific_review(uid,pid,sid)
    if (len(ratings)>0):
        return render_template('edit_review_page.html',
                            ratings=ratings,user=uid,product=pid)
    else:
        return render_template('add_review_page.html',
                            ratings=ratings,user=uid,product= str(Product.get_name(pid)[0])[2:-3],sid=sid,pid=pid)

@bp.route('/delete_review/<uid>_pid>_<sid>', methods = ['GET', 'POST'])
def delete_review(uid,pid):
    Rating.delete_review(uid,pid)
    avg = Rating.get_ratings_for_avg(pid)
    Product.update_rating(pid,avg)
    return redirect(url_for('ind_prod.show_product', k = pid))
    
@bp.route('/update_review/<uid>_<pid>_<sid>', methods = ['GET', 'POST'])
def update_review(uid,pid,sid):
    reviewvalue = request.form.get('reviewText')
    ratingvalue = Decimal(request.form.get('ratingText'))
    now = datetime.now()
    time = now.strftime("%m-%d-%Y %H:%M:%S")
    Rating.updateReview(uid,pid,sid,reviewvalue,ratingvalue,time)
    avg = Rating.get_ratings_for_avg(pid)
    Product.update_rating(pid,avg)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = "main"))

@bp.route('/add_review/<uid>_<pid>_<sid>', methods = ['GET', 'POST'])
def add_review(uid,sid,pid):
    reviewvalue = request.form.get('reviewText')
    ratingvalue = Decimal(request.form.get('ratingText'))
    now = datetime.now()
    time = now.strftime("%m-%d-%Y %H:%M:%S")
    Rating.addReview(uid,sid,pid,reviewvalue,ratingvalue,time)
    avg = Rating.get_ratings_for_avg(pid)
    Product.update_rating(pid,avg)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = "main"))

@bp.route('/view_all_reviews/<uid>', methods = ['GET', 'POST'])
def view_all(uid):
    ratings = Rating.get_user_ratings(uid)
    return render_template('all_review_page.html',
                          ratings=ratings, ratings_len=len(ratings))