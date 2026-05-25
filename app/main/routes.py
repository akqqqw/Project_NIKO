from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from app import db
from app.models import Booking, Tour, Agency
from app.utils import allowed_image, save_image

main_bp = Blueprint('main', __name__)


class ProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить')


@main_bp.route('/')
def home():
    tours = Tour.query.order_by(Tour.created_at.desc()).limit(6).all()
    agencies = Agency.query.order_by(Agency.id.desc()).limit(4).all()
    return render_template('home.html', tours=tours, agencies=agencies)


@main_bp.route('/profile')
@login_required
def profile():
    bookings = Booking.query.filter_by(user_id=current_user.id).join(Tour).all()
    return render_template('profile.html', bookings=bookings)


@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data.lower()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename and allowed_image(image.filename):
                filename = save_image(image)
                current_user.image_file = filename
        db.session.commit()
        flash('Профиль обновлен успешно.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)
