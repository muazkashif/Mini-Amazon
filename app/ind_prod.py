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
    prod_ratings = Rating.get_prod_reviews(k)
    sellers = ForSaleItems.get_sellers_for_product(k)
    if sid == "main":
        seller_info = "None"
    else:
        seller_info = ForSaleItems.get_prod_seller_info(k, sid)
        sid = int(sid)
    if (current_user.is_authenticated and len(Purchase.get_quantity_purchased(current_user.id,k))>0):
        review_button="enabled"
        return render_template('ind_product.html',
                           prod_items=prod,
                           ratings=prod_ratings,
                           sellers = sellers,
                           review_button=review_button,
                           seller_info = seller_info,
                           current_uid=current_user.id,
                           sid = sid,
                           ratingsNumber=Rating.get_number_of_ratings(k),
                           rating_sort = Rating.get_rating_sort())
    else:
        if (current_user.is_authenticated):
            curr_uid = current_user.id
        else:
            curr_uid = -1
        review_button="disabled"
        return render_template('ind_product.html',
                           prod_items=prod,
                           ratings=prod_ratings,
                           sellers = sellers,
                           review_button=review_button,
                           seller_info = seller_info,
                           current_uid=curr_uid,
                           sid = sid,
                           ratingsNumber=Rating.get_number_of_ratings(k),
                           rating_sort = Rating.get_rating_sort())


@bp.route('/ind_prod/<pid>/<sid>/add_to_cart', methods = ["POST", "GET"])
def add_to_cart(pid, sid):
    try:
        quantity = int(request.form.get('cart_quantity'))
    except ValueError:
        flash("Invalid Cart Input")
        return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))
    if quantity == 0: 
        return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))
    print(ForSaleItems.get_quantity(pid, sid))
    curr_quantity = int(ForSaleItems.get_quantity(pid, sid))
    if quantity < 0 or quantity > curr_quantity:
        flash('Invalid Quantity Amount')
        return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))
    Cart.add(current_user.id, pid, sid, quantity)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = sid))


@bp.route('/upvote_review/<uid>_<pid>_<sid>', methods = ["POST", "GET"])
def upvote_review(uid,pid,sid):
    val = Rating.getvotes_for_Review(uid,pid,sid) +1
    Rating.change_upvote_Review(uid,pid,sid,val)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = "main"))

@bp.route('/downvote_review/<uid>_<pid>_<sid>', methods = ["POST", "GET"])
def downvote_review(uid,pid,sid):
    val = Rating.getvotes_for_Review(uid,pid,sid) -1
    Rating.change_upvote_Review(uid,pid,sid,val)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = "main"))

@bp.route('/change_rating_sort/<type>/<pid>', methods = ["POST", "GET"])
def change_rating_sort(type,pid):
    Rating.change_order_by(type)
    return redirect(url_for('ind_prod.show_product', k = pid, sid = "main"))
                           


        

