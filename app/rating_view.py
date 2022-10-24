from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.rating import Rating

from flask import Blueprint
bp = Blueprint('rating', __name__)


@bp.route('/rating/')
def index():
    # get all available products for sale:
    ratings = Rating.get_all()
    return render_template('rating_view.html',
                           ratings=ratings)

@bp.route('/rating/<uid>')
def show_rating_uid(uid):
    ratings = Rating.get_recent(uid, k=5)
    return render_template('rating_view.html',
                           ratings=ratings)