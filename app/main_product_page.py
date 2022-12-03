from flask import render_template, redirect, url_for, flash, request
import datetime

from .models.products import Product
from .models.purchase import Purchase

from flask import Blueprint
from flask_paginate import Pagination


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
def fix_index():
    return redirect(url_for('main_product_page.index', k = 1))

@bp.route('/index/<k>', methods = ["POST", "GET"])
def index(k):
    # get all available products for sale:
    check = True
    if k != "1":
        offset = ((int(k) - 1) * 20) + 1
    else:
        offset = 0
        check = False
    products = Product.get_all_offset(True, offset,order_prop,order_by) 
    if products is None:
        flash('Invalid id')
        return redirect(url_for('main_product_page.index', k = 1))
    # find the products current user has bought:
    logged_in = False
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        logged_in = True
        return render_template('main_product_page.html',
                           avail_products=products,
                           curr_page = int(k),
                           next_page = (int(k) + 1),
                           prev_page = (int(k) - 1),
                           purchase_history=purchases, logged_in=logged_in,purchase_history_len=len(purchases),
                           check = check)
    else:
        purchases = None
    # render the page by adding information to the index.html file
        return render_template('main_product_page.html',
                           avail_products=products,
                           curr_page = int(k),
                           next_page = (int(k) + 1),
                           prev_page = (int(k) - 1),
                           purchase_history=purchases, logged_in=logged_in,purchase_history_len=0,
                           check = check)

@bp.route('/change_stat/<prop>_<by>', methods = ["POST", "GET"])
def inc_page(prop,by):
    global order_by
    global order_prop
    order_by = by
    order_prop = prop
    return redirect(url_for('main_product_page.index', k = 1))
    
    
    
    
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