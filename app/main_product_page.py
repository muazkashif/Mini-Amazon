from flask import render_template, redirect, url_for, flash, request
import datetime
from flask_paginate import Pagination, get_page_parameter,get_page_args
from flask_login import login_user, logout_user, current_user
from flask import current_app as app

from .models.products import Product
from .models.purchase import Purchase
from .models.for_sale import ForSaleItems
from .models.transactions import Transaction

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


@bp.route('/index', defaults = {'flag':False, 'sort': "A", 'direction':"A", 'cat':"A", 'price':"A", 'rate':"A"}, methods = ["POST", "GET"])
@bp.route('/index/<flag>_<sort>_<direction>_<cat>_<price>_<rate>', methods = ["POST", "GET"])  
def index(flag, sort, direction, cat, price, rate):
    searching = False
    sort_rate = "None"
    sort_price = "None"
    sort_purch = "None"
    searching_empty = False
    if flag:
        if sort == "Rate":
            products_for_sale = ForSaleItems.get_all_products_for_sale_rate(direction)
            sort_rate = direction
        elif sort == "Price":
            products_for_sale = ForSaleItems.get_all_products_for_sale_price(direction)
            sort_price = direction
        elif sort == "sales":
            products_for_sale = Transaction.get_all_products_for_total_sales(direction)
            sort_purch = direction
        elif sort == "filter":
            
            products_for_sale = ForSaleItems.filter_products(cat, price, rate)
        
    else:
        products_for_sale = ForSaleItems.get_all_products_for_sale() 

    if cat == "A":
        cat = "None"
    if price == "A":
        price = "None"
    if rate == "A":
        rate = "None"
    check = False
    search = False
    search_sort= request.form.get('sort_search_main')
    page, per_page, offset = get_page_args(get_page_parameter(), per_page=20)
    #products_for_sale = ForSaleItems.get_all_products_for_sale() 
    pagination_prods = get_prods(products_for_sale, False, "", offset=offset, per_page=per_page)
        
    if products_for_sale is None:
        check = True
        #searching_empty = False
        return render_template('main_product_page.html', check = check, search_term = search_sort)
    if search_sort is None or search_sort == "":
        print(rate)
        pagination = Pagination(page=page, total=len(products_for_sale), search=search, per_page=per_page)
        return render_template('main_product_page.html', avail_products = pagination_prods, css_framework='bootstrap3', pagination = pagination, search_term = search_sort, check = check,
        catfilt = cat, pricefilt = price, ratefilt = rate, sortrate = sort_rate, sortprice = sort_price, sortpurch = sort_purch) 
    else:
        searching = True
        return redirect(url_for('main_product_page.search',  searching = searching, search= request.form.get('sort_search_main')))

@bp.route('/search/<searching>_<search>', methods = ["POST", "GET"])
def search(searching, search):
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
    return render_template('main_product_page.html', avail_products = pagination_prods, css_framework='bootstrap3', pagination = pagination, search_term = search, check = check, searching = searching) 
    
@bp.route('/sort_rate/<dir>', methods = ["POST", "GET"])
def rating_sort(dir):
    if dir == "ASC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Rate", direction="ASC", cat = "A", price = "A", rate = "A"))
    if dir == "DESC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Rate", direction="DESC", cat = "A", price = "A", rate = "A" ))
    else:
        return redirect(url_for('main_product_page.index'))

@bp.route('/filter_products', methods = ["POST", "GET"])
def filtr_all():
    filter_cat = request.form.get('filter_cat')
    filter_price = request.form.get('filter_price')
    filter_rate = request.form.get('filter_rating')
    if filter_cat == "None": 
        filter_cat = "A"
    if filter_price == "None":
        filter_price = "A"
    if filter_rate == "None":
        filter_rate = "A"
    return redirect(url_for('main_product_page.index', flag = True, sort = "filter", direction = "A", cat = filter_cat, price = filter_price, rate = filter_rate))


@bp.route('/sort_price/<dir>', methods = ["POST", "GET"])
def price_sort(dir):
    if dir == "ASC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Price", direction="ASC", cat = "A", price = "A", rate = "A"))
    if dir == "DESC":
        return redirect(url_for('main_product_page.index', flag=True, sort="Price", direction="DESC", cat = "A", price = "A", rate = "A" ))
    else:
        return redirect(url_for('main_product_page.index'))
    
# @bp.route('/filter_category/<dir>', methods = ["POST", "GET"])
# def filter_category(dir):
#     return redirect(url_for('main_product_page.index', flag=True, sort="cat", direction=dir))

@bp.route('/sort_purchases/<dir>', methods = ["POST", "GET"])
def sort_by_total_purchases(dir):
    return redirect(url_for('main_product_page.index', flag=True, sort="sales", direction=dir, cat = "A", price = "A", rate = "A"))


# @bp.route('/filter_price/<dir>', methods = ["POST", "GET"])
# def filter_price(dir):
#     return redirect(url_for('main_product_page.index', flag=True, sort="pricef", direction=dir))

# @bp.route('/filter_rate/<dir>', methods = ["POST", "GET"])
# def filter_rate(dir):
#     return redirect(url_for('main_product_page.index', flag=True, sort="ratef", direction= int(dir)))
    
    
    
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