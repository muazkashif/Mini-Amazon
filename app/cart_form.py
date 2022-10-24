from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.cart import Cart


from flask import Blueprint
bp = Blueprint('cart_form', __name__)

class cart_form(FlaskForm):
    id = IntegerField('name', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/cart_form', methods=['GET', 'POST'])
def cart_search():
    form = cart_form()
    cart = None
    if form.validate_on_submit():
        info = form.id.data
        cart = Cart.get(form.id.data)
        if cart is None:
            flash('Invalid id')
            return redirect(url_for('cart_form.cart_search'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('cart.show_cart_uid', uid = info)

        return redirect(next_page)
    return render_template('cart_form.html', form=form)