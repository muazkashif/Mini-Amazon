from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.Rating import Rating


from flask import Blueprint
bp = Blueprint('rating_form', __name__)

class rating_form(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/rating_form', methods=['GET', 'POST'])
def rating_search():
    form = rating_form()
    rating = None
    if form.validate_on_submit():
        info = form.id.data
        rating = Rating.get(form.id.data)
        if rating is None:
            flash('Invalid id')
            return redirect(url_for('rating_form.rating_search'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('rating.show_rating_uid', uid = info)

        return redirect(next_page)
    return render_template('rating_form.html', form=form)