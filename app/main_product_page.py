from flask import render_template, redirect, url_for, flash, request
import datetime
from flask_paginate import Pagination, get_page_parameter,get_page_args
from flask_login import login_user, logout_user, current_user

from .models.products import Product
from .models.purchase import Purchase
from .models.for_sale import ForSaleItems

from flask import Blueprint


bp = Blueprint('main_product_page', __name__)

order_prop= "No Simple"
order_by = "No Simple"

@bp.route('/')
def opener_page():
    return render_template('opener_page.html')

@bp.route('/page_jump', methods = ["POST", "GET"])
def jump():
    page = request.form.get('Go To Page')
    total_length = len(Product.get_all()) // 20 + 1
    if int(page) < 1 or int(page) > total_length:
        flash('Invalid Page Number')
        return redirect(url_for('main_product_page.index', k = 1))
    return redirect(url_for('main_product_page.index', k = page))

@bp.route('/index', methods = ["POST", "GET"])
def index():
    check = False
    search_sort = request.form.get('sort_search_main')
    search = False
    page, per_page, offset = get_page_args(get_page_parameter(), per_page=20)
    if search_sort is None or search_sort == "":
        products_for_sale = ForSaleItems.get_all_products_for_sale() 
        pagination_prods = get_prods(False, "", offset=offset, per_page=per_page)
        search_sort = "None"
    else:
        products_for_sale = ForSaleItems.get_all_products_for_sale_search(search_sort)
        pagination_prods = get_prods(True, search_sort, offset=offset,per_page=per_page)
    if products_for_sale is None:
        check = True
        return render_template('/main_product_page.html', check = check, search_term = search_sort)
    pagination = Pagination(page=page, total=len(products_for_sale), search=search, per_page=per_page)
    return render_template('main_product_page.html', avail_products = pagination_prods, css_framework='bootstrap3', pagination = pagination, search_term = search_sort, check = check) 

def get_prods(search, term, offset, per_page):
    if search:
        products_for_sale = ForSaleItems.get_all_products_for_sale_search(term)
        if products_for_sale is None:
            return None
    else:
        products_for_sale = ForSaleItems.get_all_products_for_sale()
    return products_for_sale[offset: offset+per_page]
    
# @bp.route('/index/<k>', methods = ["POST", "GET"])
# def index(k):
#     # get all available products for sale:
#     check = True
#     if k != "1":
#         offset = ((int(k) - 1) * 20) + 1
#     else:
#         offset = 0
#         check = False
#     products = Product.get_all_offset(True, offset,order_prop,order_by) 
#     if products is None:
#         flash('Invalid id')
#         return redirect(url_for('main_product_page.index', k = 1))
#     # find the products current user has bought:
#     logged_in = False
#     if current_user.is_authenticated:
#         purchases = Purchase.get_all_by_uid_since(
#             current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
#         logged_in = True
#         return render_template('main_product_page.html',
#                            avail_products=products,
#                            curr_page = int(k),
#                            next_page = (int(k) + 1),
#                            prev_page = (int(k) - 1),
#                            purchase_history=purchases, logged_in=logged_in,purchase_history_len=len(purchases),
#                            check = check)
#     else:
#         purchases = None
#     # render the page by adding information to the index.html file
#         return render_template('main_product_page.html',
#                            avail_products=products,
#                            curr_page = int(k),
#                            next_page = (int(k) + 1),
#                            prev_page = (int(k) - 1),
#                            purchase_history=purchases, logged_in=logged_in,purchase_history_len=0,
#                            check = check)

@bp.route('/change_stat/<prop>_<by>', methods = ["POST", "GET"])
def inc_page(prop,by):
    global order_by
    global order_prop
    order_by = by
    order_prop = prop
    return redirect(url_for('main_product_page.index', k = 1))
    return
    
    
    
    
@bp.route('/index/rate/DESC')
def sort_rate_best():
    products = Product.sort_ratings_desc()
    return render_template('main_product_page.html',
                           avail_products = products)

@bp.route('/index/rate/ASC')
def sort_rate_worst():
    products = Product.sort_ratings_asc()
    return render_template('main_product_page.html',
                           avail_products = products)

@bp.route('/index/price/DESC')
def sort_product_expensive():
    products = Product.sort_price_desc()
    return render_template('main_product_page.html',
                           avail_products = products)

@bp.route('/index/price/ASC')
def sort_rate_cheap():
    products = Product.sort_price_asc()
    return render_template('main_product_page.html',
                           avail_products = products)

@bp.route('/index/category/<cat>')
def sort_category(cat):
    products = Product.get_prod_category(cat)
    return render_template('main_product_page.html',
                           avail_products = products)