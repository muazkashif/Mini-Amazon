from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('purchases_form', __name__)

class purchases_form(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/purchases_form', methods=['GET', 'POST'])
def purchases_search():
    form = purchases_form()
    purchases = None
    if form.validate_on_submit():
        info = form.id.data
        purchases = Purchase.get_all_purchases_by_uid(form.id.data)
        if purchases is None:
            flash('Invalid id')
            return redirect(url_for('purchases_form.purchases_search'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('purchases.show_purchases_given_uid', uid = info)

        return redirect(next_page)
    return render_template('purchases_form.html', form=form)