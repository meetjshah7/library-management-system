from flask import render_template, request
from . import book
from ...models import Books
from sqlalchemy import or_


@book.route("/search", methods=["GET", "POST"])
def search():
    """
    Perform a search for books based on a query.

    Returns:
        Renders the 'book/books.html' template with the search results.
    """

    page = request.args.get("page", 1, type=int)
    query = request.form.get("search")
    if query is None:
        query = request.args.get("search")
    books = (
        Books.query.filter(
            or_(Books.title.contains(query), Books.author.contains(query))
        )
        .order_by(Books.id.asc())
        .paginate(page=page, per_page=5)
    )
    return render_template("book/books.html", title=query, books=books, is_search=True)
