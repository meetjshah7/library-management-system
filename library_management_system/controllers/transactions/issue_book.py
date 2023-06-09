from flask import flash, redirect, render_template, request, url_for
from wtforms import FloatField, Form, SelectField, validators

from library_management_system import db

from ...models import Books, Members, Transactions
from . import transaction


class IssueBook(Form):
    book_id = SelectField("Book ID", choices=[])
    member_id = SelectField("Member ID", choices=[])
    per_day_rent = FloatField("Per Day Renting Fee", [validators.NumberRange(min=1)])


@transaction.route("/issue_book", methods=["GET", "POST"])
def issue_book():
    """
    Issue a book to a member.

    Returns:
        Renders the 'Issue Book' template with the form to issue a book.

        If the request method is POST and the form is valid, it adds a new transaction to the database
        and updates the book's issued count. If successful, it redirects to the 'All Transactions' route.
        If the book is not available for renting, it renders the template with an error message.
    """

    form: IssueBook = IssueBook(request.form)

    books: Books = Books.query.all()
    book_list = []

    for book in books:
        book_tuple = (book.id, book.title)
        book_list.append(book_tuple)

    members: Members = Members.query.all()
    member_list = []
    for member in members:
        member_tuple = (member.id, member.name)
        member_list.append(member_tuple)

    form.book_id.choices = book_list
    form.member_id.choices = member_list

    if request.method == "POST" and form.validate():
        book_to_issue: Books = Books.query.get(form.book_id.data)
        copies_available_for_renting = book_to_issue.quantity - book_to_issue.issued

        if copies_available_for_renting == 0:
            error = "No copies of this book are availabe to be rented"
            return render_template(
                "transaction/issue_book.html", form=form, error=error
            )

        new_transaction = Transactions(
            member_id=form.member_id.data,
            book_id=form.book_id.data,
            per_day_rent=form.per_day_rent.data,
        )
        db.session.add(new_transaction)
        book_to_issue.issued += 1

        db.session.commit()

        flash("Book Issued", "success")
        return redirect(url_for("transaction.all_transactions"))

    return render_template("transaction/issue_book.html", form=form)
