from flask import render_template

from .models.products import Product
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('product', __name__)


@bp.route('/products/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # # find the products current user has bought:
    # if current_user.is_authenticated:
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # else:
    #     purchases = None
    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        return render_template('products_for_cart.html',
                           prod_items=products)
    return render_template('products.html',
                           prod_items=products)

@bp.route('/products/<k>')
def show_product_top(k):
    prod = Product.get_top_k_products(k)
    return render_template('products.html',
                           prod_items=prod)

