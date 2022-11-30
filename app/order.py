from flask import render_template, request
from flask_login import current_user
import datetime

from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('order', __name__)


@bp.route('/order/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form.get("trash"):
                print("hi")
                Purchase.remove(current_user.id, request.form.get("trash"))
            if request.form.getlist("selectfromcart"):
                print("hello")
                for pid in request.form.getlist("selectfromcart"):
                    p = ""
                    sid = ""
                    quantity = ""
                    count = 0
                    for i in range(1, len(pid)-1):
                        if pid[i] == ",":
                            count += 1
                        if pid[i] != "," and pid[i] != " ":
                            if count == 0:
                                p = p + pid[i]
                            elif count == 1:
                                sid = sid + pid[i]
                            else:
                                quantity = quantity + pid[i]
                        
                    Purchase.add(current_user.id, int(p), int(sid), int(quantity))
    purchases = Purchase.get_all()
    if current_user.is_authenticated:
        purchases = Purchase.get_all_purchases_by_uid(current_user.id)
        return render_template('orders.html',
                            purchases=purchases, logged_in=True)
    return render_template('orders.html',
                            purchases=purchases)