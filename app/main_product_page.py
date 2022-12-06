from flask import render_template, redirect, url_for, flash, request
import datetime
from flask_paginate import Pagination, get_page_parameter,get_page_args
from flask_login import login_user, logout_user, current_user
from flask import current_app as app

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


@bp.route('/index', defaults = {'flag':False, 'sort': "", 'direction':""}, methods = ["POST", "GET"])
@bp.route('/index/<flag>_<sort>_<direction>', methods = ["POST", "GET"])  
def index(flag, sort, direction):
    if flag:
        if sort == "Rate":
            products_for_sale = ForSaleItems.get_all_products_for_sale_rate(direction)
            print(products_for_sale)
        elif sort == "Price":
            if direction == "ASC":
                products_for_sale = ForSaleItems.get_all_products_for_sale_price(direction)
            else:
               products_for_sale = ForSaleItems.get_all_products_for_sale_price(direction)
    else:
        products_for_sale = ForSaleItems.get_all_products_for_sale() 
    check = False
    search = False
    search_sort= request.form.get('sort_search_main')
    page, per_page, offset = get_page_args(get_page_parameter(), per_page=20)
    #products_for_sale = ForSaleItems.get_all_products_for_sale() 
    pagination_prods = get_prods(products_for_sale, False, "", offset=offset, per_page=per_page)
        
    if products_for_sale is None:
        check = True
        return render_template('/main_product_page.html', check = check, search_term = search_sort)
    if search_sort is None or search_sort == "":
        pagination = Pagination(page=page, total=len(products_for_sale), search=search, per_page=per_page)
        return render_template('main_product_page.html', avail_products = pagination_prods, css_framework='bootstrap3', pagination = pagination, search_term = search_sort, check = check) 
    else:
        return redirect(url_for('main_product_page.search', search= request.form.get('sort_search_main')))

@bp.route('/search/<search>', methods = ["POST", "GET"])
def search(search):
    # search= request.form.get('sort_search_main')
    check = False
    page, per_page, offset = get_page_args(get_page_parameter(), per_page=20)
    
    products_for_sale = ForSaleItems.get_all_products_for_sale_search(search) 
    # print(len(products_for_sale))
    pagination_prods = get_prods(products_for_sale, True, search, offset=offset, per_page=per_page)
        
    if products_for_sale is None:
        check = True
        return render_template('/main_product_page.html', check = check, search_term = search)
    pagination = Pagination(page=page, total=len(products_for_sale), search=False, per_page=per_page)
    return render_template('main_product_page.html', avail_products = pagination_prods, css_framework='bootstrap3', pagination = pagination, search_term = search, check = check) 
    
@bp.route('/sort_rate/<dir>', methods = ["POST", "GET"])
def rating_sort(dir):
    if dir == "ASC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Rate", direction="ASC"))
    if dir == "DESC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Rate", direction="DESC" ))
    else:
        return redirect(url_for('main_product_page.index'))

@bp.route('/sort_price/<dir>', methods = ["POST", "GET"])
def price_sort(dir):
    if dir == "ASC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Price", direction="ASC"))
    if dir == "DESC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Price", direction="DESC" ))
    else:
        return redirect(url_for('main_product_page.index'))
    
    
    
def get_prods(products_for_sale, search, term, offset, per_page):
    if search:
        products_for_sale = ForSaleItems.get_all_products_for_sale_search(term)
        if products_for_sale is None:
            return None
    #else:
        #products_for_sale = ForSaleItems.get_all_products_for_sale()
    return products_for_sale[offset: offset+per_page]
    

# @bp.route('/change_stat/<prop>_<by>', methods = ["POST", "GET"])
# def inc_page(prop,by):
#     global order_by
#     global order_prop
#     order_by = by
#     order_prop = prop
#     return redirect(url_for('main_product_page.index', k = 1))
#     return
    
    

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