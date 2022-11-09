from flask import render_template, request
from flask_login import current_user
import datetime

from ..models.products import Product
from ..models.purchase import Purchase
from ..models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            form = request.form.getlist("addtocart2")
            products = Product.get_all()
            for i in range(len(form)):
                if int(form[i]) != 0:
                    Cart.add(current_user.id, products[i].id, 2, int(form[i]))
        
            for pid in request.form.getlist("removefromcart"):
                Cart.remove(current_user.id, pid)
            # for pid in request.form.getlist("addtocart"):
            #     Cart.add(current_user.id, pid, 2, 1)        
    # get all available products for sale:
    carts = Cart.get_all()
    if current_user.is_authenticated:
        carts = Cart.get(current_user.id)
        prices = []
        for i in range(len(carts)):
            item = carts[i]
            prices.append(item.quantity * Product.get(item.pid).price)
        return render_template('carts.html',
                            cart_items=carts, cart_len=len(carts), prices=prices, logged_in=True)
    return render_template('carts.html',
                            cart_items=carts)

@bp.route('/carte/')
def show_emptycart():
    carts = Cart.get_all()
    if current_user.is_authenticated:
        Cart.clear(current_user.id)
        carts = Cart.get(current_user.id)
        return render_template('carts.html',
                            cart_items=carts, logged_in=True)
    return render_template('carts.html',
                            cart_items=carts)

@bp.route('/cart/<uid>')
def show_cart_uid(uid):
    carts = Cart.get(uid)
    return render_template('carts.html',
                           cart_items=carts)