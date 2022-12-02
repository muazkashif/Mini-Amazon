from flask import render_template, request
from flask_login import current_user
import datetime

from .models.purchase import Purchase
from .models.cart import Cart
from .models.for_sale import ForSaleItems

from flask import Blueprint
bp = Blueprint('order', __name__)


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


@bp.route('/order/checkout', methods=['GET','POST'])
def check_out_all():
    cart = Cart.get(current_user.id)
    for item in cart:
        pid, sid, quantity = item.pid, item.sid, item.quantity
        price = float(ForSaleItems.get_price(pid, sid)[0])
        quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
        new_quantity = quantity_available - int(quantity)
        if new_quantity >= 0:
            Purchase.add(current_user.id, int(pid), int(sid), int(quantity))
            Cart.delete_product_cart(current_user.id, int(pid), int(sid))
            ForSaleItems.remove(pid, sid, quantity_available, price)
            ForSaleItems.add(pid, sid, new_quantity, price)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)

@bp.route('/order/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                pid, sid, quantity = translate(request.form.get("trash"))
                Purchase.remove(current_user.id, int(pid), int(sid))
            elif request.form.getlist("selectfromcart"):
                for id in request.form.getlist("selectfromcart"):
                    pid, sid, quantity = translate(id)
                    price = float(ForSaleItems.get_price(pid, sid)[0])
                    quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
                    new_quantity = quantity_available - int(quantity)
                    if new_quantity >= 0:
                        Purchase.add(current_user.id, int(pid), int(sid), int(quantity))
                        Cart.delete_product_cart(current_user.id, int(pid), int(sid))
                        ForSaleItems.remove(pid, sid, quantity_available, price)
                        ForSaleItems.add(pid, sid, new_quantity, price)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)