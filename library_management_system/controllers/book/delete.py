from flask import flash, redirect, url_for

from library_management_system import db

from ...models import Books
from . import book


@book.route("/delete/<string:id>", methods=["POST"])
def delete_book(id):
    """
    Delete a book from the library.

    Args:
        id (str): The ID of the book to be deleted.

    Returns:
        Redirects to the route for displaying all books.
    """

    try:
        Books.query.filter(Books.id == id).delete()
        db.session.commit()
    except Exception as e:
        print(e)

        flash("Book could not be deleted", "danger")
        flash(str(e), "danger")

        return redirect(url_for("book.all_books"))

    flash("Book Deleted", "success")

    return redirect(url_for("book.all_books"))
