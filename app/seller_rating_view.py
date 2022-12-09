from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.rating import Rating
from .models.transactions import Transaction
from .models.user import User

from flask import Blueprint
bp = Blueprint('seller_rating_view', __name__)


@bp.route('/seller_reviews/')
def index():
    # get all available products for sale:
    ratings = Rating.get_seller_ratings()
    return render_template('user_rating_view.html',
                           ratings=ratings, check = False)

@bp.route('/seller_reviews/<sid>', methods=['GET','POST'])
def show_rating_uid(sid):
    ratings = Rating.get_seller_ratings(sid)
    check = False
    if ratings is None: 
        check = True
    counts = Transaction.getCountForSid(sid)
    user_info = User.get(sid)
    total = Rating.get_ratings_seller_avg(sid)
    if total is None:
        total = "N/A"
    else:
        total = round(total, 2)
    return render_template('seller_rating_view.html',
                           ratings=ratings, sid = sid, counts=counts, info=user_info, check = check, total = total) 