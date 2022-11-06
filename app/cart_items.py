from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart/')
def index():
    # get all available products for sale:
    carts = Cart.get_all()
    if current_user.is_authenticated:
        carts = Cart.get(current_user.id)
        return render_template('carts.html',
                            cart_items=carts)
    return render_template('carts.html',
                            cart_items=carts)
    

@bp.route('/cart/<uid>')
def show_cart_uid(uid):
    carts = Cart.get(uid)
    return render_template('carts.html',
                           cart_items=carts)