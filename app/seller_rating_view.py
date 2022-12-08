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
    ratings = Rating.get_all()
    return render_template('user_rating_view.html',
                           ratings=ratings)

@bp.route('/seller_reviews/<sid>', methods=['GET','POST'])
def show_rating_uid(sid):
    ratings = Rating.get_seller_ratings(sid)
    counts = Transaction.getCountForSid(sid)
    user_info = User.get(sid)
    return render_template('seller_rating_view.html',
                           ratings=ratings, sid = sid, counts=counts, info=user_info) 