from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchases', __name__)

@bp.route('/purchases/')
def index():
    purchases = Purchase.get_all()
    return render_template('purchases.html',
                           purchase_history=purchases, purchase_history_len=len(purchases))

@bp.route('/purchases/<uid>')
def show_purchases_given_uid(uid):
    purchases = Purchase.get_all_purchases_by_uid(uid)
    return render_template('purchases.html', 
                            purchase_history=purchases,purchase_history_len=len(purchases))