from flask import flash, redirect, render_template, request, url_for
from library_management_system.controllers.book.add_edit_form import AddBook
from . import book
from ...models import Books
from library_management_system import db


@book.route('/add', methods=['GET', 'POST'])
def add_book():

    form: AddBook = AddBook(request.form)

    if request.method == 'POST' and form.validate():

        new_book = Books(
            {
                'bookID': form.book_id.data,
                'isbn': form.isbn.data,
                'isbn13': form.isbn13.data,
                'title': form.title.data,
                'quantity': form.quantity.data,
                'authors': form.author.data,
                'average_rating': form.average_rating.data,
                'language_code': form.language_code.data,
                '  num_pages': form.num_pages.data,
                'ratings_count': form.ratings_count.data,
                'text_reviews_count': form.text_reviews_count.data,
                'publication_date': form.publication_date.data,
                'publisher': form.publisher.data
            },
            quantity=form.quantity.data
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book Added", "success")

        return redirect(url_for('book.all_books'))

    return render_template('book/add_book.html', form=form, book=book)
