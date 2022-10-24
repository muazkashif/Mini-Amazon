from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.seller import Seller


from flask import Blueprint
bp = Blueprint('seller_form', __name__)

class seller_form(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/seller_form', methods=['GET', 'POST'])
def seller_search():
    form = seller_form()
    seller = None
    if form.validate_on_submit():
        info = form.id.data
        seller = Seller.get(form.id.data)
        if seller is None:
            flash('Invalid id')
            return redirect(url_for('seller_form.seller_search'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('seller.show_seller_uid', sid = info)

        return redirect(next_page)
    return render_template('seller_form.html', form=form)