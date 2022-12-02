from flask import render_template, request
from flask_login import current_user
import datetime

from ..models.products import Product
from ..models.purchase import Purchase
from ..models.for_sale import ForSaleItems
from ..models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


def translate(id):
    p = ""
    sid = ""
    quantity = ""
    count = 0
    for i in range(1, len(id)-1):
        if id[i] == ",":
            count += 1
        if id[i] != "," and id[i] != " ":
            if count == 0:
                p = p + id[i]
            elif count == 1:
                sid = sid + id[i]
            else:
                quantity = quantity + id[i]
    return p, sid, quantity

@bp.route('/cart/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                pid, sid, uid = translate(request.form.get("trash"))
                Cart.delete_product_cart(int(uid), int(pid), int(sid))
            form = request.form.getlist("addtocart2")
            items = ForSaleItems.get_all()
            for i in range(len(form)):
                if int(form[i]) != 0:
                    quantity_available = ForSaleItems.get_quantity(items[i].pid, items[i].sid)[0][0]
                    if int(form[i]) <= quantity_available:
                        Cart.add(current_user.id, items[i].pid, items[i].sid, int(form[i]))

    carts = Cart.get_all()
    if current_user.is_authenticated:
        carts = Cart.get(current_user.id)
        return render_template('carts.html',
                            cart_items=carts, cart_len=len(carts), logged_in=True)
    return render_template('carts.html',
                            cart_items=carts)


@bp.route('/carte/')
def show_emptycart():
    carts = Cart.get_all()
    if current_user.is_authenticated:
        Cart.clear(current_user.id)
        carts = Cart.get(current_user.id)
        return render_template('carts.html',
                            cart_items=carts, cart_len=len(carts), prices=[], logged_in=True)
    return render_template('carts.html',
                            cart_items=carts)

@bp.route('/cart/<uid>')
def show_cart_uid(uid):
    carts = Cart.get(uid)
    return render_template('carts.html',
                           cart_items=carts)