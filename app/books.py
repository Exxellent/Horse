import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Book, BookGenre, Review, User, Genre, Image
from tools import ImageSaver, ReviewsFilter
from auth import check_rights
import markdown
import bleach

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 3

COMMENT_PAGE = 5

PER_PAGE_COMMENTS = 10

BOOK_PARAMS = ['author', 'name', 'publisher',
               'short_desc', 'year', 'vol_pages']

COMMENT_PARAMS = ['rating', 'text', 'book_id', 'user_id']

COLLECTION_PARAMS = ['name', 'user_id']


def params():
    return {p: request.form.get(p) for p in BOOK_PARAMS}


def comment_params():
    return {p: request.form.get(p) for p in COMMENT_PARAMS}


def search_params_comm(book_id, req_form=None):
    return {
        'name': request.args.get('name'),
        'book_id': book_id,
        'sort': req_form
    }





def add_genre_to_book(book_id, genre_id):
    return {
        'book_id': book_id,
        'genre_id': genre_id
    }


@bp.route('/new')
@check_rights('create')
@login_required
def new():
    genres = Genre.query.all()
    return render_template('books/new.html', genres=genres, form={}, genres_select=[])


@bp.route('/create', methods=['POST'])
@check_rights('create')
@login_required
def create():
    book = Book(**params())
    # экранирование запрещенных тегов
    book.short_desc = bleach.clean(book.short_desc)
    try:
        db.session.add(book)
        db.session.commit()
    except:
        db.session.rollback()
        genres = Genre.query.all()
        genres_select = request.form.getlist('genre')
        for i in range(len(genres_select)):
            genres_select[i] = int(genres_select[i])
        flash('При сохранении книги произошла ошибка. Проверьте введённые данные.', 'danger')
        return render_template('books/new.html', genres=genres, form=params(), genres_select=genres_select)

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save(book.id)
        if img == None:
            db.session.delete(book)
            db.session.commit()
            genres = Genre.query.all()
            genres_select = request.form.getlist('genre')
            for i in range(len(genres_select)):
                genres_select[i] = int(genres_select[i])
            flash('Нельзя использовать книгу с обложкой, которая уже имеется!', 'danger')
            return render_template('books/new.html', genres=genres, form=params(), genres_select=genres_select)
    else:
        db.session.delete(book)
        db.session.commit()
        genres = Genre.query.all()
        genres_select = request.form.getlist('genre')
        for i in range(len(genres_select)):
            genres_select[i] = int(genres_select[i])
        flash('Книга не может быть без обложки. Загрузите обложку!', 'danger')
        return render_template('books/new.html', genres=genres, form=params(), genres_select=genres_select)
    
    # добавление выбранных жанров из multiple списком id
    genres_arr = request.form.getlist('genre')
    for genres in genres_arr:
        book_genre = BookGenre(**add_genre_to_book(book.id, genres))
        db.session.add(book_genre)

    db.session.commit()

    flash(f'Книга {book.name} была успешно добавлена!', 'success')
    return redirect(url_for('index'))


@bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    # преобразование текста из html в markdown
    book.short_desc = markdown.markdown(book.short_desc)
    reviews = Review.query.filter_by(book_id=book_id).limit(
        COMMENT_PAGE)  # подгружаем несколько отзывов
    for review in reviews:
        review.text = markdown.markdown(review.text)
    user_review = None
    if current_user.is_authenticated is True:
        # проверка написал ли пользователь данной сессии комментарий
        user_review = Review.query.filter_by(
            book_id=book_id, user_id=current_user.id).first()
        
        if user_review:
            user_review.text = markdown.markdown(user_review.text)

    genres_quer = BookGenre.query.filter_by(
        book_id=book_id).all()  # берем все жанры у этой книги
    genres = []
    for genre in genres_quer:
        genres.append(genre.genre.name)
    genres = ', '.join(genres)

    # подгружаем картинку книги
    img = Image.query.filter_by(book_id=book_id).first()
    img = img.url
    

    return render_template('books/show.html', book=book, review=reviews, user_review=user_review, genres=genres, image=img)


@bp.route('/<int:book_id>/edit')
@login_required
@check_rights('update')
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    genres_quer = BookGenre.query.filter_by(book_id=book_id).all() # выбранные жанры у книги
    genres_select = []
    for genre in genres_quer:
        genres_select.append(genre.genre.id)

    return render_template('books/edit.html', genres=genres, form={}, genres_select=genres_select, book=book)


@bp.route('/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights('update')
def update(book_id):  
    book = Book.query.filter_by(id=book_id).first()  # апдейт книги
    form_dict = params()
    book.name = form_dict['name']
    book.author = form_dict['author']
    book.publisher = form_dict['publisher']
    book.short_desc = form_dict['short_desc']
    # экранирование запрещенных тегов
    book.short_desc = bleach.clean(book.short_desc)
    book.year = form_dict['year']
    book.vol_pages = form_dict['vol_pages']

    # удаление старых жанров для данной книги
    genres_old = BookGenre.query.filter_by(book_id=book_id).all()
    for gnr in genres_old:
        db.session.delete(gnr)

    # добавление новых жанров для данной книги
    genres_arr = request.form.getlist('genre')
    for genres in genres_arr:
        book_genre = BookGenre(**add_genre_to_book(book.id, genres))
        db.session.add(book_genre)

    db.session.commit()
    flash(f'Вы успешно отредактировали книгу {book.name}!', 'success')
    return redirect(url_for('index'))


@bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
@check_rights('delete')
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book_name = book.name
    img = Image.query.filter_by(book_id=book_id).first()
    img_path = os.path.join(os.path.dirname(os.path.abspath(
        __file__)), 'media', 'images') + '/' + img.storage_filename # удаление картинки из папки media
    db.session.delete(book)
    db.session.commit()
    os.remove(img_path)
    flash(f'Книга {book_name} была успешно удалена!', 'success')
    return redirect(url_for('index'))


@bp.route('/<int:book_id>/send_comment', methods=['POST'])
@login_required
@check_rights('check_collections')
def send_comment(book_id):
    reviews = Review(**comment_params())
    # экранирование запрещенных тегов
    reviews.text = bleach.clean(reviews.text)

    book = Book.query.filter_by(id=book_id).first()
    book.rating_num += 1
    book.rating_sum += int(reviews.rating)
    try:
        db.session.add(reviews)
        db.session.commit()
    except:
        db.session.rollback()
        flash(f'Не удалось добавить комментарий!', 'danger')
        return redirect(url_for('books.show', book_id=book.id))
    flash('Комментарий был успешно добавлен!', 'success')
    return redirect(url_for('books.show', book_id=book.id))


@bp.route('/<int:book_id>/reviews')
def reviews(book_id):
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort')
    reviews = ReviewsFilter(book_id).sort_reviews(sort)
    books = Book.query.filter_by(id=book_id).first()
    pagination = reviews.paginate(page, PER_PAGE_COMMENTS)
    reviews = pagination.items
    return render_template('books/reviews.html', reviews=reviews, books=books, req_form=sort, pagination=pagination, search_params=search_params_comm(book_id, sort))


def take_info_for_card_book(books):
    imgs_arr = []
    genres_arr = []
    for book in books:
        img = Image.query.filter_by(book_id=book.id).first()
        imgs_arr.append(img.url)
        genres_quer = BookGenre.query.filter_by(book_id=book.id).all()
        genres = []
        for genre in genres_quer:
            genres.append(genre.genre.name)
        genres_str = ', '.join(genres)
        genres_arr.append(genres_str)
    return imgs_arr, genres_arr