from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_paginate import Pagination, get_page_parameter,get_page_args

from .models.products import Product
from .models.for_sale import ForSaleItems
from flask_login import current_user
from .models.transactions import Transaction
from flask_login import login_user, logout_user

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


@bp.route('/add_product_now', methods = ['POST', 'GET'])
def add_product_current():
    product_name = request.form.get('new_product_name')
    product_description = request.form.get('new_product_description')
    product_category = request.form.get('trans')
    product_image = request.form.get('new_product_image')
    if product_name == "" or product_description == "" or product_category == "" or product_category is None or product_image == "":
        flash("Invalid Product Information")
        return redirect(url_for('product.add_product'))
    try:
        product_price = float(request.form.get('new_product_price'))
        product_quantity = int(request.form.get('new_product_quantity'))
    except ValueError:
        flash("Invalid quantity or price input")
        return redirect(url_for('product.add_product'))
    if product_price < 0 or product_quantity < 0:
        flash("Invalid quantity or price input")
        return redirect(url_for('product.add_product'))
    pid = Product.add_new_product(product_name, product_description, product_category, 1, product_image, True)
    if pid is None:
        flash("Invalid Name. Already Exists")
        return redirect(url_for('product.add_product'))
    ForSaleItems.add_new_sale(pid, current_user.id, product_quantity, product_price)
    return redirect(url_for('users.see_seller_products'))

    
@bp.route('/sell_a_product', methods = ['POST', 'GET'])
def become_seller_for_product():
    check = False
    search_sort = request.form.get('sort_search_existing')
    search = False
    page, per_page, offset = get_page_args(get_page_parameter(), per_page=100)
    if search_sort is None or search_sort == "":
        products_for_sale = Product.get_all()
        pagination_prods = get_prods(False, "", offset=offset, per_page=per_page)
        search_sort = "None"
    else:
        products_for_sale = Product.get_all_search(search_sort)
        pagination_prods = get_prods(True, search_sort, offset=offset,per_page=per_page)
    if products_for_sale is None:
        check = True
        return render_template('become_prod_seller.html', check = check, search_term = search_sort)
    pagination = Pagination(page=page, total=len(products_for_sale), search=search, per_page=per_page)
    return render_template('become_prod_seller.html', all_products = pagination_prods, css_framework='bootstrap3', pagination = pagination, search_term = search_sort, check = check)

def get_prods(search, term, offset, per_page):
    if search:
        products_for_sale = Product.get_all_search(term)
        if products_for_sale is None:
            return None
    else:
        products_for_sale = Product.get_all()
    return products_for_sale[offset: offset+per_page]

@bp.route('/add_seller_form/<pid>', methods = ['POST', 'GET'])
def add_seller_for_prod(pid):
    return render_template('add_seller_form.html', pid = pid)

@bp.route('/add_seller_form_now/<pid>', methods = ['POST', 'GET'])
def add_seller_form_query(pid):
    try:
        product_price = float(request.form.get('existing_product_price'))
        product_quantity = int(request.form.get('existing_product_quantity'))
    except ValueError:
        flash("Invalid quantity or price input")
        return redirect(url_for('product.add_seller_for_prod', pid = pid))
    if product_price < 0 or product_quantity < 0:
        flash("Invalid quantity or price input")
        return redirect(url_for('product.add_seller_for_prod', pid = pid))
    already_seller = ForSaleItems.add_new_sale(pid, current_user.id, product_quantity, product_price)
    if already_seller is None: 
        flash("Already Seller For This Item; Please Edit If Necessary")
        return redirect(url_for('users.see_seller_products'))
    return redirect(url_for('users.see_seller_products'))

@bp.route('/product_edit/<pid>', methods = ['POST', 'GET'])
def edit_product_info(pid):
    product_info = Product.get(pid)
    seller_info = ForSaleItems.get_prod_seller_info(pid, current_user.id)
    return render_template('edit_product_info.html', product = product_info, seller = seller_info)
    

@bp.route('/update_product_now/<pid>', methods = ['POST', 'GET'])
def update_product_info(pid):
    product_name = request.form.get('new_product_name')
    product_description = request.form.get('new_product_description')
    product_category = request.form.get('trans')
    product_image = request.form.get('new_product_image')
    product_info = Product.get(pid)
    if product_category is None:
        product_category = product_info.category
    if product_name == "" or product_description == "" or product_category == "" or product_image == "":
        flash("Invalid Product Descriptions")
        return redirect(url_for('product.edit_product_info', pid = pid))
    try:
        product_price = float(request.form.get('new_product_price'))
        product_quantity = int(request.form.get('new_product_quantity'))
    except ValueError:
        flash("Invalid quantity or price input")
        return redirect(url_for('product.edit_product_info', pid = pid))
    if product_price < 0 or product_quantity < 0:
        flash("Invalid quantity or price input")
        return redirect(url_for('product.edit_product_info', pid = pid))
    Product.update_product(pid, product_name, product_description, product_category, product_image, 1, True)
    ForSaleItems.update_sale(pid, current_user.id, product_price, product_quantity)
    return redirect(url_for('users.see_seller_products'))

