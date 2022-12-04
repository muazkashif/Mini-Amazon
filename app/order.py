from flask import render_template, request
from flask_login import current_user
from datetime import datetime

from .models.purchase import Purchase
from .models.cart import Cart
from .models.for_sale import ForSaleItems
from .models.user import User

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
    success = False
    cart = Cart.get(current_user.id)
    total_price = 0
    balance = User.get_balance(current_user.id)
    for item in cart: 
        pid, sid, quantity = item.pid, item.sid, item.quantity
        quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
        new_quantity = quantity_available - int(quantity)
        if new_quantity >= 0:
            total_price += float(ForSaleItems.get_price(pid, sid)[0]) * item.quantity
    if total_price < balance:
        success = True
        User.updateBalance(current_user.id, float(balance)-total_price)
        time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        for item in cart:
            pid, sid, quantity = item.pid, item.sid, item.quantity
            seller_balance = User.get_balance(sid)
            price = float(ForSaleItems.get_price(pid, sid)[0])
            User.updateBalance(item.sid, float(seller_balance) + price*int(quantity))
            quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
            new_quantity = quantity_available - int(quantity)
            if new_quantity >= 0:
                Purchase.add(current_user.id, int(pid), int(sid), int(quantity), time)
                Cart.delete_product_cart(current_user.id, int(pid), int(sid))
                ForSaleItems.remove(pid, sid, quantity_available, price)
                ForSaleItems.add(pid, sid, new_quantity, price)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        if success:
            purchases = Purchase.get_order(current_user.id, time)
        else:
            purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)

@bp.route('/order/', methods=['GET','POST'])
def index():
    success = False
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                pid, sid, quantity = translate(request.form.get("trash"))
                Purchase.remove(current_user.id, int(pid), int(sid))
            elif request.form.getlist("selectfromcart"):
                total_price = 0
                balance = User.get_balance(current_user.id)
                for id in request.form.getlist("selectfromcart"): 
                    pid, sid, quantity = translate(id)
                    quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
                    new_quantity = quantity_available - int(quantity)
                    if new_quantity >= 0:
                        total_price += float(ForSaleItems.get_price(pid, sid)[0]) * int(quantity)
                if total_price < balance:
                    success = True
                    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    User.updateBalance(current_user.id, float(balance)-total_price)
                    for id in request.form.getlist("selectfromcart"):
                        pid, sid, quantity = translate(id)
                        seller_balance = User.get_balance(sid)
                        price = float(ForSaleItems.get_price(pid, sid)[0])
                        User.updateBalance(sid, float(seller_balance) + int(quantity)*price)
                        quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
                        new_quantity = quantity_available - int(quantity)
                        if new_quantity >= 0:
                            Purchase.add(current_user.id, int(pid), int(sid), int(quantity), time)
                            Cart.delete_product_cart(current_user.id, int(pid), int(sid))
                            ForSaleItems.remove(pid, sid, quantity_available, price)
                            ForSaleItems.add(pid, sid, new_quantity, price)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        if success:
            purchases = Purchase.get_order(current_user.id, time)
        else:
            purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)