import hashlib
import uuid
from models import Book, Image, Review, BookGenre
import os
from werkzeug.utils import secure_filename
from app import db, app
import markdown


class BooksFilter:
    def __init__(self):
        self.query_name = Book.query

    def perform(self):
        return self.query_name.order_by(Book.name.desc())



class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self, book_id):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return None
        file_name = secure_filename(self.file.filename)
        self.img = Image(id=str(uuid.uuid4()), file_name=file_name,
                         mime_type=self.file.mimetype, md5_hash=self.md5_hash)
        self.file.save(os.path.join(app.config['UPLOAD_FOLDER'], self.img.storage_filename))
        self.img.book_id = book_id
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Image.query.filter(Image.md5_hash == self.md5_hash).first()


class ReviewsFilter:
    def __init__(self, book_id):
        self.query = Review.query.filter_by(book_id=book_id)

    def sort_reviews(self, sort):
        reviews = self.__perform_date_desc()
        if sort == 'old':
            reviews = self.__perform_date_asc()
        elif sort == 'good':
            reviews = self.__perform_rating_desc()
        elif sort == 'bad':
            reviews = self.__perform_rating_asc()
        for review in reviews:
            review.text = markdown.markdown(review.text)
        return reviews

    def __perform_date_desc(self):
        return self.query.order_by(Review.created_at.desc())

    def __perform_date_asc(self):
        return self.query.order_by(Review.created_at.asc())

    def __perform_rating_desc(self):
        return self.query.order_by(Review.rating.desc())

    def __perform_rating_asc(self):
        return self.query.order_by(Review.rating.asc())
