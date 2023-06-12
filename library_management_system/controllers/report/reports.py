from flask import render_template
from . import report
from ...models import Books, Members, Transactions
from sqlalchemy import func


@report.route("/reports")
def reports():
    """
    Generate various reports based on book and member data.

    Returns:
        Renders the 'report/reports.html' template with the generated reports,
        including the top books by rating, newest books, popular books, books with minimum
        copies remaining, top members by amount spent, and top members by outstanding amount.
    """

    top_books_by_rating = (
        Books.query.order_by(Books.average_rating.desc()).limit(5).all()
    )
    newest_books = Books.query.order_by(Books.publication_date.desc()).limit(5).all()
    top_members_by_amount_spent = (
        Members.query.order_by(Members.amount_spent.desc()).limit(5).all()
    )
    top_members_by_outstanding_amount = (
        Members.query.order_by(Members.amount_spent.desc()).limit(5).all()
    )
    popular_books = (
        Transactions.query.with_entities(
            Books, Transactions.book_id, func.count(Transactions.id)
        )
        .join(Books, Transactions.book_id == Books.id)
        .group_by(Transactions.book_id)
        .order_by(-1 * func.count(Transactions.id))
        .all()
    )

    books_with_min_copies_remaining = (
        Books.query.order_by((Books.quantity - Books.issued).asc()).limit(5).all()
    )

    return render_template(
        "report/reports.html",
        title="Reports",
        top_books_by_rating=top_books_by_rating,
        newest_books=newest_books,
        popular_books=popular_books,
        books_with_min_copies_remaining=books_with_min_copies_remaining,
        top_members_by_amount_spent=top_members_by_amount_spent,
        top_members_by_outstanding_amount=top_members_by_outstanding_amount,
    )
