from flask import render_template

from ...models import Books
from . import book


@book.route("/view/<string:id>")
def view_book(id):
    """
    Display the details of a book.

    Parameters:
        id (str): The ID of the book.

    Returns:
        Renders the 'Book Details' template with the book details.
    """

    book = Books.query.get(id)

    if book is not None:
        return render_template("book/view_book.html", book=book)
    else:
        msg = "This book Does Not Exist"
        return render_template("book/view_book.html", warning=msg)
