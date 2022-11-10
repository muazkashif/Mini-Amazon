from flask import render_template, request
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('order', __name__)


@bp.route('/order/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                Purchase.remove(current_user.id, request.form.get("trash"))
            if request.form.getlist("selectfromcart"):
                for pid in request.form.getlist("selectfromcart"):
                    #CHANGE THIS TO TRANSACTION BEHAVIOR
                    Purchase.add(current_user.id, pid, 2, 1)
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)