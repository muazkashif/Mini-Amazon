from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.products import Product


from flask import Blueprint
bp = Blueprint('product_form', __name__)

class product_form(FlaskForm):
    k = IntegerField('How Many Products?', validators=[DataRequired()])
    submit = SubmitField('Search')

#Need limit on max k?

@bp.route('/product_form', methods=['GET', 'POST'])
def product_search():
    form = product_form()
    if form.validate_on_submit():
        k_top = form.k.data
        prod = Product.get_top_k_products(form.k.data)
        if prod is None:
            flash('Invalid k')
            return redirect(url_for('product_form.product_search')) 
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('product.show_product_top', k = k_top) 
        
        return redirect(next_page)
    return render_template('product_form.html', form=form)