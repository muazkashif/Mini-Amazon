from flask import render_template

from .models.products import Product
from flask_login import current_user
from .models.rating import Rating

from flask import Blueprint
bp = Blueprint('ind_prod', __name__)


@bp.route('/ind_prod/')
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
    # print(products)
    # print(products[0].id)
    # if current_user.is_authenticated:
    #     return render_template('products_for_cart.html',
    #                        prod_items=products)
    # return render_template('products.html',
    #                        prod_items=products)

@bp.route('/ind_prod/<k>', methods = ["POST", "GET"])
def show_product(k):
    prod = Product.get(k)
    ratings = Rating.get_prod_reviews(k)
    return render_template('ind_product.html',
                           prod_items=prod,
                           ratings = ratings)

