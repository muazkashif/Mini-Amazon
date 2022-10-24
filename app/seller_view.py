from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('seller', __name__)


@bp.route('/seller/')
def index():
    sell = Seller.get_all()
    return render_template('seller.html',
                           seller_items=sell)

@bp.route('/seller/<sid>')
def show_seller_sid(sid):
    sellers = Seller.get_inventory_by_sid(sid)
    return render_template('seller.html',
                           seller_items=sellers)
