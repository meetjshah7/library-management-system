from flask import render_template
from . import book
from ...models import Books


@book.route("/view/<string:id>")
def viewBook(id):
    """
    Display the details of a book.

    Parameters:
        id (str): The ID of the book.

    Returns:
        Renders the 'book/view_book.html' template with the book details.
    """

    book = Books.query.get(id)

    if book is not None:
        return render_template("book/view_book.html", book=book)
    else:
        msg = "This book Does Not Exist"
        return render_template("book/view_book.html", warning=msg)
