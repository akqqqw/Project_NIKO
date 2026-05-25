import math
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

from app import db
from app.models import Tour, Agency, Booking
from app.utils import allowed_image, save_image, admin_required

tours_bp = Blueprint('tours', __name__)


class SearchForm(FlaskForm):
    query = StringField('Поиск', validators=[Length(max=100)])
    submit = SubmitField('Найти')


class TourForm(FlaskForm):
    title = StringField('Название тура', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Описание', validators=[DataRequired(), Length(min=20)])
    country = StringField('Страна', validators=[DataRequired(), Length(max=100)])
    duration = StringField('Длительность', validators=[DataRequired(), Length(max=50)])
    price = DecimalField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    agency_id = SelectField('Турагентство', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')


@tours_bp.route('/')
def tour_list():
    page = request.args.get('page', 1, type=int)
    search_text = request.args.get('q', '', type=str)
    query = Tour.query.order_by(Tour.created_at.desc())
    if search_text:
        query = query.filter(
            or_(
                Tour.title.ilike(f'%{search_text}%'),
                Tour.country.ilike(f'%{search_text}%'),
                Tour.description.ilike(f'%{search_text}%')
            )
        )
    pagination = query.paginate(page=page, per_page=6, error_out=False)
    return render_template('tours.html', pagination=pagination, q=search_text)


@tours_bp.route('/<int:tour_id>')
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template('tour_detail.html', tour=tour)


@tours_bp.route('/book/<int:tour_id>', methods=['POST'])
@login_required
def book_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    existing = Booking.query.filter_by(user_id=current_user.id, tour_id=tour.id).first()
    if existing:
        flash('Тур уже добавлен в ваши бронирования.', 'info')
        return redirect(url_for('tours.tour_detail', tour_id=tour.id))
    booking = Booking(user_id=current_user.id, tour_id=tour.id)
    db.session.add(booking)
    db.session.commit()
    flash('Тур добавлен в ваши бронирования.', 'success')
    return redirect(url_for('main.profile'))


@tours_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tour():
    form = TourForm()
    form.agency_id.choices = [(agency.id, agency.name) for agency in Agency.query.order_by(Agency.name).all()]
    if form.validate_on_submit():
        tour = Tour(
            title=form.title.data,
            description=form.description.data,
            country=form.country.data,
            duration=form.duration.data,
            price=float(form.price.data),
            agency_id=form.agency_id.data,
        )
        if 'image' in request.files:
            image = request.files['image']
            if image.filename and allowed_image(image.filename):
                tour.image_file = save_image(image)
        db.session.add(tour)
        db.session.commit()
        flash('Тур успешно создан.', 'success')
        return redirect(url_for('tours.tour_list'))
    return render_template('edit_tour.html', form=form, action='Добавить тур')


@tours_bp.route('/<int:tour_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = TourForm(obj=tour)
    form.agency_id.choices = [(agency.id, agency.name) for agency in Agency.query.order_by(Agency.name).all()]
    if form.validate_on_submit():
        tour.title = form.title.data
        tour.description = form.description.data
        tour.country = form.country.data
        tour.duration = form.duration.data
        tour.price = float(form.price.data)
        tour.agency_id = form.agency_id.data
        if 'image' in request.files:
            image = request.files['image']
            if image.filename and allowed_image(image.filename):
                tour.image_file = save_image(image)
        db.session.commit()
        flash('Тур обновлен.', 'success')
        return redirect(url_for('tours.tour_detail', tour_id=tour.id))
    return render_template('edit_tour.html', form=form, tour=tour, action='Редактировать тур')


@tours_bp.route('/<int:tour_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    db.session.delete(tour)
    db.session.commit()
    flash('Тур удален.', 'success')
    return redirect(url_for('tours.tour_list'))
