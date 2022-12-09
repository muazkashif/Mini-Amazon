from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
import datetime

from ..models.products import Product
from ..models.purchase import Purchase
from ..models.for_sale import ForSaleItems
from ..models.cart import Cart
from ..models.coupons import Coupons

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

@bp.route('/coupon_apply', methods=['GET','POST'])
def add_coupon():
    descrp = "None"
    effect = "None"
    check = False
    form = request.form.get("coupon")
    discount = Coupons.get_effect(form)
    #print(discount)
    if discount is None: 
        flash("Invalid Coupon Code")
        return redirect(url_for("cart.index"))
    if discount[0][1] == "None":
        descrp = discount[0][2]
        effect = 1 - discount[0][3]
    elif discount[0][2] == "None":
        descrp = discount[0][1]
        effect = 1 - discount[0][3]
    pid_cat_avail = Cart.get_pid_category(current_user.id)
    print(pid_cat_avail)
    for idx in range(len(pid_cat_avail)):
        if descrp == pid_cat_avail[idx][0] or descrp == pid_cat_avail[idx][1] or descrp == "All":
            flash("Coupon Successfully Applied!")
            check = True
            return redirect(url_for("cart.index", descrp = descrp, effect = effect, check = check))
    flash("Invalid Coupon Code")
    return redirect(url_for("cart.index"))

@bp.route('/cart/', defaults = {'descrp':None, 'effect':None, 'check':False}, methods=['GET','POST'])
@bp.route('/cart/<descrp>_<effect>_<check>', methods=['GET','POST'])
def index(descrp, effect, check):
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                pid, sid, uid = translate(request.form.get("trash"))
                Cart.delete_product_cart(int(uid), int(pid), int(sid))
            form = request.form.getlist("addtocart2")
            items = ForSaleItems.get_all()
            for i in range(len(form)):
                if int(form[i]) != 0:
                    quantity_available = items[i].quantity
                    if int(form[i]) <= quantity_available:
                        Cart.add(current_user.id, items[i].pid, items[i].sid, int(form[i]))

    carts = Cart.get_all()
    if current_user.is_authenticated:
        carts = Cart.get(current_user.id)
        product_names = []
        prices = []
        unit_price = []
        total_price = 0
        for item in carts:
            product_info = Product.get(item.pid) 
            product_names.append(Product.get_name(item.pid)[0][0])
            if descrp == product_info.category or descrp == str(item.pid) or descrp == "All":
                unit_price.append(round(float(ForSaleItems.get_price(item.pid, item.sid)[0]) * float(effect), 2))
                price_no_effect = item.quantity * float(ForSaleItems.get_price(item.pid, item.sid)[0])
                price_with_effect_round = round(price_no_effect * float(effect), 2)
                price_temp_round = price_with_effect_round
                prices.append(price_with_effect_round)
                total_price += price_temp_round
            else:
                unit_price.append(round(float(ForSaleItems.get_price(item.pid, item.sid)[0]), 2))
                price_no_effect = item.quantity * float(ForSaleItems.get_price(item.pid, item.sid)[0])
                price_round = round(price_no_effect, 2)
                prices.append(price_round)
                total_price +=  price_round
        return render_template('carts.html',
                            cart_items=carts, cart_len=len(carts), product_names=product_names,prices=prices,logged_in=True, total_price=round(total_price,2), check = check, unit_price = unit_price)
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