from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.rating import Rating

from flask import Blueprint
bp = Blueprint('user_rating_view', __name__)



@bp.route('/all_reviews/')
def index():
    # get all available products for sale:
    ratings = Rating.get_all()
    return render_template('rating_view.html',
                           ratings=ratings)


@bp.route('/user_reviews/<uid>')
def show_rating_uid(uid):
    ratings = Rating.get_recent_uid(uid, k=5)
    return render_template('user_rating_view.html',
                           ratings=ratings)