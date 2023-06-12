from flask import flash, redirect, render_template, request, url_for
from wtforms import Form, SelectField, FloatField, validators
from . import transaction
from ...models import Books, Members, Transactions
from library_management_system import db


class IssueBook(Form):
    book_id = SelectField('Book ID', choices=[])
    member_id = SelectField('Member ID', choices=[])
    per_day_rent = FloatField('Per Day Renting Fee', [validators.NumberRange(min=1)])


@transaction.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    # Get form data from request
    form: IssueBook = IssueBook(request.form)

    books: Books = Books.query.all()
    book_list = []

    for book in books:
        t = (book.id, book.title)
        book_list.append(t)

    members: Members = Members.query.all()
    member_list = []
    for member in members:
        t = (member.id, member.name)
        member_list.append(t)

    form.book_id.choices = book_list
    form.member_id.choices = member_list

    # To handle POST request to route
    if request.method == 'POST' and form.validate():

        book: Books = Books.query.get(form.book_id.data)
        copies_available_for_renting = book.quantity - book.issued

        if copies_available_for_renting == 0:
            error = 'No copies of this book are availabe to be rented'
            return render_template('transaction/issue_book.html', form=form, error=error)
        
        new_transaction = Transactions(
            member_id=form.member_id.data,
            book_id=form.book_id.data,
            per_day_rent=form.per_day_rent.data
        )
        db.session.add(new_transaction)

        book.issued += 1

        db.session.commit()

        flash("Book Issued", "success")

        return redirect(url_for('transaction.all_transactions'))

    # To handle GET request to route
    return render_template('transaction/issue_book.html', form=form)