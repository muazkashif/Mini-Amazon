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

@bp.route('/order/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                pid, sid, quantity = translate(request.form.get("trash"))
                Purchase.remove(current_user.id, int(pid), int(sid))
            if request.form.getlist("selectfromcart"):
                for id in request.form.getlist("selectfromcart"):
                    pid, sid, quantity = translate(id)
                    quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))[0][0]
                    new_quantity = quantity_available - int(quantity)
                    if new_quantity >= 0:
                        Purchase.add(current_user.id, int(pid), int(sid), int(quantity))
                        Cart.delete_product_cart(current_user.id, int(pid), int(sid))
                        ForSaleItems.remove(pid, sid, quantity_available)
                        ForSaleItems.add(pid, sid, new_quantity)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)