from flask import render_template, request
from library_management_system.models import Books
from . import book
from sqlalchemy import or_


@book.route('/list')
def all_books():
    page = request.args.get('page', 1, type=int)
    books = Books.query.order_by(Books.id.asc()).paginate(page=page, per_page=5)
    return render_template('book/books.html', books=books, is_search=False)
