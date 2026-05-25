from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import User, Tour, Agency
from app.utils import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    user_count = User.query.count()
    tour_count = Tour.query.count()
    agency_count = Agency.query.count()
    return render_template('admin_dashboard.html', user_count=user_count, tour_count=tour_count, agency_count=agency_count)


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.order_by(User.name).all()
    return render_template('admin_users.html', users=users)


@admin_bp.route('/users/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
@admin_required
def toggle_user_admin(user_id):
    if current_user.id == user_id:
        flash('Нельзя изменять права текущего администратора.', 'warning')
        return redirect(url_for('admin.manage_users'))
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Права пользователя обновлены.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/tours')
@login_required
@admin_required
def manage_tours():
    tours = Tour.query.order_by(Tour.created_at.desc()).all()
    return render_template('admin_tours.html', tours=tours)


@admin_bp.route('/agencies')
@login_required
@admin_required
def manage_agencies():
    agencies = Agency.query.order_by(Agency.name).all()
    return render_template('admin_agencies.html', agencies=agencies)
