from datetime import datetime
from typing import cast

from flask import flash, redirect, render_template, request, url_for
from wtforms import FloatField, Form, validators

from library_management_system import db

from ...models import Books, Members, Transactions
from . import transaction


class ReturnBook(Form):
    amount_paid = FloatField("Amount Paid", [validators.NumberRange(min=0)])


@transaction.route("/return_book/<string:transaction_id>", methods=["GET", "POST"])
def return_book(transaction_id):
    """
    Return the issued book

    Parameters:
        transaction_id (str): The ID of the transaction for returning the book.

    Returns:
        If the request method is GET, it renders the 'Return Book' template
        with the return book form containing the necessary transaction details.

        If the request method is POST and the form is valid, it processes the return book transaction.
        On Success, it redirects to the 'All Transactions' endpoint.
        On any Error, it renders the 'Return Book' template with the error message.
    """

    form: ReturnBook = ReturnBook(request.form)
    transaction: Transactions = cast(Transactions, db.session.get(Transactions, transaction_id))

    current_date = datetime.now()
    difference = current_date - cast(datetime, transaction.issued_on)
    difference_in_days = difference.days
    total_charge = difference_in_days * transaction.per_day_rent

    if request.method == "POST" and form.validate():
        amount_to_be_settled = total_charge - form.amount_paid.data
        member: Members = cast(Members, db.session.get(Members, transaction.member_id))

        outstanding_debt = member.outstanding_debt

        if outstanding_debt + amount_to_be_settled > 500:
            error = "Outstanding Debt Cannot Exceed Rs.500"
            return render_template(
                "transaction/return_book.html",
                form=form,
                error=error,
                total_charge=total_charge,
                transaction=transaction,
            )

        transaction.returned_on = current_date
        transaction.amount_settled += form.amount_paid.data
        transaction.total_rent = total_charge
        transaction.book_returned = True

        member.outstanding_debt += amount_to_be_settled
        member.amount_spent += form.amount_paid.data

        book: Books = cast(Books, db.session.get(Books, transaction.book_id))
        book.issued -= 1

        db.session.commit()

        flash("Book Returned", "success")
        return redirect(url_for("transaction.all_transactions"))

    return render_template(
        "transaction/return_book.html",
        form=form,
        total_charge=total_charge,
        difference=difference,
        transaction=transaction,
    )
