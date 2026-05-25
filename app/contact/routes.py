from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from app import db
from app.models import ContactMessage

contact_bp = Blueprint('contact', __name__)


class ContactForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Отправить')


@contact_bp.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data.lower(),
            message=form.message.data,
        )
        db.session.add(message)
        db.session.commit()
        flash('Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.', 'success')
        return redirect(url_for('contact.contact'))
    return render_template('contact.html', form=form)
