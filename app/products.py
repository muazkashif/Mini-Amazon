from flask import render_template, redirect, url_for

from .models.products import Product
from .models.for_sale import ForSaleItems
from flask_login import current_user
from .models.transactions import Transaction

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
        items = ForSaleItems.get_all()
        prices = []
        names = []
        for temp in items:
            names.append(Product.get_name(temp.pid)[0][0])
            prices.append(Product.get_price(temp.pid)[0][0])
        return render_template('products_for_cart.html',
                           prod_items=items, prices=prices, names=names, product_len=len(names))
    return render_template('products.html',
                           prod_items=products)

@bp.route('/products/<k>')
def show_product_top(k):
    prod = Product.get_top_k_products(k)
    return render_template('products.html',
                           prod_items=prod)


@bp.route('/product_delete/<k>', methods = ['POST', 'GET'])
def delete_product(k):
    Product.delete_product_seller(k, current_user.id)
    return redirect(url_for('users.see_seller_products'))

# @bp.route('/product_edit/<k>', methods = ['POST', 'GET'])
# def edit_product(k):
#     Product.delete_product_seller(k, current_user.id)
#     return redirect(url_for('users.see_seller_products'))

@bp.route('/change_status/<stat>/<uid>/<pid>/<time>', methods = ['POST', 'GET'])
def change_status(stat, uid, pid, time):
    Transaction.update_status(stat, current_user.id, uid, pid, time)
    return redirect(url_for('users.see_seller_transactions'))

@bp.route('/add_product', methods = ['POST', 'GET'])
def add_product():
    return render_template('new_products.html')


