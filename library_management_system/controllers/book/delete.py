from flask import flash, redirect, url_for
from . import book
from library_management_system import db
from ...models import Books


@book.route('/delete/<string:id>', methods=['POST'])
def delete_book(id):
    try:
        db.session.query(Books).filter(Books.id==id).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        
        flash("Book could not be deleted", "danger")
        flash(str(e), "danger")

        return redirect(url_for('book.all_books'))

    flash("Book Deleted", "success")

    return redirect(url_for('book.all_books'))