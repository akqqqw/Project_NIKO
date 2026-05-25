import os
from functools import wraps
from flask import current_app, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename


def allowed_image(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']


def save_image(file_storage, folder_name='uploads'):
    filename = secure_filename(file_storage.filename)
    if not allowed_image(filename):
        return None
    upload_folder = current_app.config['UPLOAD_FOLDER']
    path = os.path.join(upload_folder, filename)
    file_storage.save(path)
    return filename


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Доступ разрешен только для администратора.', 'danger')
            return redirect(url_for('main.home'))
        return view_func(*args, **kwargs)
    return wrapper
