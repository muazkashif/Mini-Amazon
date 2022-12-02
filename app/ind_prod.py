from flask import render_template, request, redirect, url_for, flash

from .models.products import Product
from flask_login import current_user
from .models.rating import Rating
from .models.purchase import Purchase
from .models.seller import Seller
from .models.for_sale import ForSaleItems
from .models.cart import Cart
from .models.for_sale import ForSaleItems

from flask import Blueprint
bp = Blueprint('ind_prod', __name__)


#@bp.route('/ind_prod/')
#def index():
    # get all available products for sale:
    #products = Product.get_all(True)
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

@bp.route('/ind_prod/<k>/<sid>', methods = ["POST", "GET"])
def show_product(k, sid):
    prod = Product.get(k)
    ratings = Rating.get_prod_reviews(k)
    sellers = ForSaleItems.get_sellers_for_product(k)
    if sid == "main":
        seller_info = "None"
    else:
        seller_info = ForSaleItems.get_prod_seller_info(k, sid)
    if (current_user.is_authenticated and len(Purchase.get_quantity_purchased(current_user.id,k))>0):
        review_button="enabled"
        return render_template('ind_product.html',
                           prod_items=prod,
                           ratings=ratings,
                           sellers = sellers,
                           review_button=review_button,
                           seller_info = seller_info,
                           current_uid=current_user.id,
                           ratingsNumber=Rating.get_number_of_ratings(k))
    else:
        if (current_user.is_authenticated):
            curr_uid = current_user.id
        else:
            curr_uid = -1
        review_button="disabled"
        return render_template('ind_product.html',
                           prod_items=prod,
                           ratings=ratings,
                           sellers = sellers,
                           review_button=review_button,
                           seller_info = seller_info,
                           current_uid=curr_uid,
                           ratingsNumber=Rating.get_number_of_ratings(k))


@bp.route('/ind_prod/<pid>/<sid>/add_to_cart', methods = ["POST", "GET"])
def add_to_cart(pid, sid):
    quantity = int(request.form.get('cart_quantity'))
    #check is provided value is an integer
    if quantity == 0: 
        return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))
    curr_quantity = int(ForSaleItems.get_quantity(pid, sid))
    if quantity < 0 or quantity > curr_quantity:
        flash('Invalid Quantity Amount')
        return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))
    Cart.add(current_user.id, pid, sid, quantity)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))
                           


        

