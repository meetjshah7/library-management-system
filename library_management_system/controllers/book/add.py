from flask import flash, redirect, render_template, request, url_for

from library_management_system import db
from library_management_system.controllers.book.add_edit_form import AddBook

from ...models import Books
from . import book


@book.route("/add", methods=["GET", "POST"])
def add_book():
    """
    Add a new book to the library.

    Methods:
        GET: Display the form to add a new book.
        Returns:
            render_template: Renders the 'Add Book' template with the form and book data.

        POST: Handle the submission of the form and add the book to the database.
        Returns:
            redirect: Redirects to the route for displaying all books.
    """

    form: AddBook = AddBook(request.form)

    if request.method == "POST" and form.validate():
        new_book = Books(
            {
                "bookID": form.book_id.data,
                "isbn": form.isbn.data,
                "isbn13": form.isbn13.data,
                "title": form.title.data,
                "quantity": form.quantity.data,
                "authors": form.author.data,
                "average_rating": form.average_rating.data,
                "language_code": form.language_code.data,
                "num_pages": form.num_pages.data,
                "ratings_count": form.ratings_count.data,
                "text_reviews_count": form.text_reviews_count.data,
                "publication_date": form.publication_date.data,
                "publisher": form.publisher.data,
            },
            quantity=form.quantity.data,
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book Added", "success")

        return redirect(url_for("book.all_books"))

    return render_template("book/add_book.html", form=form, book=book)
