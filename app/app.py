import os
from flask import Flask, render_template, abort, send_from_directory, render_template, request
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from books import bp as books_bp
from auth import bp as auth_bp, init_login_manager

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)


init_login_manager(app)

from models import Image
from tools import BooksFilter
from books import PER_PAGE, take_info_for_card_book

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = BooksFilter().perform()
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    # print('-----------------------------------', books)
    imgs_arr, genres_arr = take_info_for_card_book(books)
    return render_template('books/index.html', books=books, pagination=pagination, imgs=imgs_arr, genres=genres_arr)



@app.route('/media/images/<image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], image.storage_filename)
