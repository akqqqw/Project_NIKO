# Travel Agency Website

Учебный проект туристического агентства на Flask, SQLite, SQLAlchemy и Tailwind CSS.

## Установка

1. Создайте виртуальное окружение:

```bash
python -m venv venv
```

2. Активируйте окружение:

Windows:
```bash
venv\\Scripts\\activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте базу данных и таблицы:

```bash
python create_db.py
```

Если вы хотите использовать Python shell напрямую, выполните:

```bash
python
>>> from run import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

5. Запустите приложение:

```bash
python run.py
```

6. Откройте в браузере:

```
http://127.0.0.1:5000
```

## Структура проекта

- `app/` — основное приложение Flask
- `app/auth/` — маршруты регистрации и входа
- `app/main/` — главные публичные маршруты
- `app/tours/` — управление турами и поиск
- `app/agencies/` — управление туристическими агентствами
- `app/admin/` — административная панель
- `app/contact/` — форма обратной связи
- `app/templates/` — HTML шаблоны
- `app/static/` — CSS, загрузка изображений

## Важно

- Папка `app/static/uploads` используется для сохранения изображений.
- Для администратора можно вручную изменить поле `is_admin` в таблице `User`.
