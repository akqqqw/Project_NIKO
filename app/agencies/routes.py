from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from app import db
from app.models import Agency
from app.utils import allowed_image, save_image, admin_required

agencies_bp = Blueprint('agencies', __name__)


class AgencyForm(FlaskForm):
    name = StringField('Название агентства', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Описание', validators=[DataRequired(), Length(min=20)])
    contact_info = StringField('Контакты', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Сохранить')


@agencies_bp.route('/')
def agency_list():
    agencies = Agency.query.order_by(Agency.name).all()
    return render_template('agencies.html', agencies=agencies)


@agencies_bp.route('/<int:agency_id>')
def agency_detail(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    return render_template('agency_detail.html', agency=agency)


@agencies_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_agency():
    form = AgencyForm()
    if form.validate_on_submit():
        agency = Agency(
            name=form.name.data,
            description=form.description.data,
            contact_info=form.contact_info.data,
        )
        if 'image' in request.files:
            image = request.files['image']
            if image.filename and allowed_image(image.filename):
                agency.image_file = save_image(image)
        db.session.add(agency)
        db.session.commit()
        flash('Агентство добавлено.', 'success')
        return redirect(url_for('agencies.agency_list'))
    return render_template('edit_agency.html', form=form, action='Добавить агентство')


@agencies_bp.route('/<int:agency_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_agency(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    form = AgencyForm(obj=agency)
    if form.validate_on_submit():
        agency.name = form.name.data
        agency.description = form.description.data
        agency.contact_info = form.contact_info.data
        if 'image' in request.files:
            image = request.files['image']
            if image.filename and allowed_image(image.filename):
                agency.image_file = save_image(image)
        db.session.commit()
        flash('Агентство обновлено.', 'success')
        return redirect(url_for('agencies.agency_detail', agency_id=agency.id))
    return render_template('edit_agency.html', form=form, agency=agency, action='Редактировать агентство')


@agencies_bp.route('/<int:agency_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_agency(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    db.session.delete(agency)
    db.session.commit()
    flash('Агентство удалено.', 'success')
    return redirect(url_for('agencies.agency_list'))
