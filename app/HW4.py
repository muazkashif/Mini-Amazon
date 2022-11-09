from flask import render_template
from flask_login import current_user
import datetime

from .models.products import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('HW4', __name__)


@bp.route('/hw4')
def HW4():
    return render_template('HW4.html')