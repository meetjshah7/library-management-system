from datetime import datetime
from library_management_system import db


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False, unique=True)
    isbn13 = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    issued = db.Column(db.Integer, nullable=False, default=0)
    author = db.Column(db.String(255), nullable=False)
    added = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)
    average_rating = db.Column(db.Integer, nullable=True)
    language_code = db.Column(db.String(10), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    ratings_count = db.Column(db.Integer, nullable=False)
    text_reviews_count = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)

    def __init__(self, book, quantity):
        self.book_id = book['bookID']
        self.isbn = book['isbn']
        self.isbn13 = book['isbn13']
        self.title = book['title']
        self.quantity = quantity
        self.author = book['authors']
        self.average_rating = book['average_rating']
        self.language_code = book['language_code']
        self.num_pages = book['  num_pages']
        self.ratings_count = book['ratings_count']
        self.text_reviews_count = book['text_reviews_count']
        if isinstance(book['publication_date'], str):
            self.publication_date = datetime.strptime(book['publication_date'], "%m/%d/%Y")
        else:
            self.publication_date = book['publication_date']
        self.publisher = book['publisher']


class Members(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    outstanding_debt = db.Column(db.Integer, nullable=False)
    amount_spent = db.Column(db.Integer, nullable=False)
    books = db.relationship('Transactions', backref='members', lazy=True)
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)

    def __init__(self, member):
        self.name = member['name']
        self.email = member['email']
        self.outstanding_debt = member['outstanding_debt']
        self.amount_spent = member['amount_spent']


class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    issued_on = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)
    returned_on = db.Column(db.DateTime(timezone=True))
    book_returned = db.Column(db.Boolean, nullable=False, default=False)
    per_day_rent = db.Column(db.Integer, nullable=False, default=0)
    total_rent = db.Column(db.Integer, nullable=False, default=0)
    amount_settled = db.Column(db.Integer, nullable=False, default=0)
    updated_on = db.Column(db.DateTime(timezone=True), onupdate=datetime.now(), default=datetime.now(), nullable=False)

    def __init__(self, member_id, book_id, per_day_rent):
        self.member_id = member_id
        self.book_id = book_id
        self.per_day_rent = per_day_rent
