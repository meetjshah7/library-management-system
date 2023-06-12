from flask import flash, redirect, render_template, request, url_for
from library_management_system.controllers.book.add_edit_form import AddBook
from . import book
from ...models import Books
from library_management_system import db


@book.route("/edit/<string:id>", methods=["GET", "POST"])
def edit_book(id):
    form: AddBook = AddBook(request.form)

    book: Books = Books.query.get(id)

    if request.method == "POST" and form.validate():
        book.book_id = form.book_id.data
        book.isbn = form.isbn.data
        book.isbn13 = form.isbn13.data
        book.title = form.title.data
        book.quantity = form.quantity.data
        book.author = form.author.data
        book.average_rating = form.average_rating.data
        book.language_code = form.language_code.data
        book.num_pages = form.num_pages.data
        book.ratings_count = form.ratings_count.data
        book.text_reviews_count = form.text_reviews_count.data
        book.publication_date = form.publication_date.data
        book.publisher = form.publisher.data

        db.session.commit()

        flash("Book Updated", "success")

        return redirect(url_for("book.all_books"))

    return render_template("book/edit_book.html", form=form, book=book)
