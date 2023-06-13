import requests
from flask import flash, redirect, render_template, request, url_for
from wtforms import Form, IntegerField, StringField, validators

from library_management_system import db

from ...models import Books
from . import book


class ImportBooks(Form):
    no_of_books = IntegerField("No. of Books*", [validators.NumberRange(min=1)])
    quantity_per_book = IntegerField(
        "Quantity Per Book*", [validators.NumberRange(min=1)]
    )
    title = StringField(
        "Title", [validators.Optional(), validators.Length(min=2, max=255)]
    )
    author = StringField(
        "Author(s)", [validators.Optional(), validators.Length(min=2, max=255)]
    )
    isbn = StringField(
        "ISBN", [validators.Optional(), validators.Length(min=10, max=10)]
    )
    publisher = StringField(
        "Publisher", [validators.Optional(), validators.Length(min=2, max=255)]
    )


def import_books_via_frappe_API(parameters):
    url = "https://frappe.io/api/method/frappe-library"
    r = requests.get(url=url, params=parameters)
    res = r.json()

    if not res["message"]:
        return None

    return res["message"]


def is_book_already_added(book_id):
    book = Books.query.filter_by(book_id=book_id).first()
    if book is None:
        return False
    return True


@book.route("/import", methods=["GET", "POST"])
def import_books():
    form: ImportBooks = ImportBooks(request.form)

    if request.method == "POST" and form.validate():
        parameters = {"page": 1}
        if form.title.data:
            parameters["title"] = form.title.data
        if form.author.data:
            parameters["author"] = form.author.data
        if form.isbn.data:
            parameters["isbn"] = form.isbn.data
        if form.publisher.data:
            parameters["publisher"] = form.publisher.data

        books_imported_currently = 0
        duplicated_book_ids = []

        while books_imported_currently != form.no_of_books.data:
            books = import_books_via_frappe_API(parameters=parameters)
            if books is None:
                break
            for single_book in books:
                if is_book_already_added(single_book["bookID"]):
                    duplicated_book_ids.append(single_book["bookID"])
                else:
                    single_book["num_pages"] = single_book["  num_pages"]
                    new_book = Books(
                        book=single_book, quantity=form.quantity_per_book.data
                    )
                    db.session.add(new_book)
                    books_imported_currently += 1
                    if books_imported_currently == form.no_of_books.data:
                        break
            parameters["page"] += 1

        db.session.commit()

        msg = f"{books_imported_currently}/{form.no_of_books.data} books have been imported"
        msgType = "success"

        if books_imported_currently != form.no_of_books.data:
            msgType = "warning"
            if len(duplicated_book_ids) > 0:
                msg += f"{len(duplicated_book_ids)} books were found with already exisiting IDs."
            else:
                msg += f"{form.no_of_books.data - books_imported_currently} matching books were not found."

        flash(msg, msgType)

        return redirect(url_for("book.all_books"))

    return render_template("book/import_books.html", form=form)
