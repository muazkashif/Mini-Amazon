from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart/')
def index():
    # get all available products for sale:
    carts = Cart.get_all()
    # # find the products current user has bought:
    # if current_user.is_authenticated:
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # else:
    #     purchases = None
    # render the page by adding information to the index.html file
    print(carts)
    print(carts[0].pid)
    return render_template('carts.html',
                           cart_items=carts)