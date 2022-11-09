from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('main_product_page', __name__)

@bp.route('/')
def opener_page():
    return render_template('opener_page.html')

@bp.route('/index')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    logged_in = False
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        logged_in = True
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('main_product_page.html',
                           avail_products=products,
                           purchase_history=purchases, logged_in=logged_in)