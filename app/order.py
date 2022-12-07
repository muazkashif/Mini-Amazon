from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
from datetime import datetime

from .models.purchase import Purchase
from .models.cart import Cart
from .models.products import Product
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
    success_price = False
    success_quantity = True
    cart = Cart.get(current_user.id)
    total_price = 0
    balance = User.get_balance(current_user.id)
    for item in cart: 
        pid, sid, quantity = item.pid, item.sid, item.quantity
        quantity_available = ForSaleItems.get_quantity(int(pid), int(sid))
        new_quantity = quantity_available - int(quantity)
        if new_quantity >= 0:
            total_price += float(ForSaleItems.get_price(pid, sid)[0]) * item.quantity
        else:
            success_quantity = False
    if total_price < balance:
        success_price = True
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
                Purchase.add(current_user.id, int(pid), int(sid), int(quantity), price, time)
                Cart.delete_product_cart(current_user.id, int(pid), int(sid))
                ForSaleItems.remove(pid, sid, quantity_available, price)
                ForSaleItems.add(pid, sid, new_quantity, price)
    purchases = Purchase.get_all()

    if current_user.is_authenticated:
        product_names = []
        if success_price:
            purchases = Purchase.get_order(current_user.id, time)
            for item in purchases:
                product_names.append(Product.get_name(item.pid)[0][0])
            all_processed = True
            for item in purchases:
                if item.order_status == "Processing":
                    all_processed = False
            if all_processed:
                message = "Complete"
            else:
                message = "Incomplete"
            if not success_quantity:
                flash("***NOTICE: Some Items In Your Purchase No Longer Available***")
            return render_template('orders.html',
                                purchases=purchases, logged_in=True, processed_info=message, product_names=product_names, purchase_len=len(product_names))
        else:
            flash("Purchase Failed: Insufficient Funds or Empty Selection")
            return redirect(url_for('cart.index'))
    return render_template('orders.html',
                            purchases=purchases)

@bp.route('/order/', methods=['GET','POST'])
def index():
    success_price = False
    success_quantity = True
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
                    else:
                        success_quantity = False
                if total_price < balance:
                    success_price = True
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
                            Purchase.add(current_user.id, int(pid), int(sid), int(quantity), price, time)
                            Cart.delete_product_cart(current_user.id, int(pid), int(sid))
                            ForSaleItems.remove(pid, sid, quantity_available, price)
                            ForSaleItems.add(pid, sid, new_quantity, price)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        product_names = []
        if success_price:
            purchases = Purchase.get_order(current_user.id, time)
            for item in purchases:
                product_names.append(Product.get_name(item.pid)[0][0])
            all_processed = True
            for item in purchases:
                if item.order_status == "Processing":
                    all_processed = False
            if all_processed:
                message = "Complete"
            else:
                message = "Incomplete"
            if not success_quantity:
                flash("***NOTICE: Some Items In Your Purchase No Longer Available***")
            return render_template('orders.html',
                                purchases=purchases, logged_in=True, processed_info=message, product_names=product_names, purchase_len=len(product_names))
        else:
            flash("Purchase Failed: Insufficient Funds or Empty Selection")
            return redirect(url_for('cart.index'))
    return render_template('orders.html',
                            purchases=purchases)