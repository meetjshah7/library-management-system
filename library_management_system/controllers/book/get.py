from flask import render_template
from . import book
from ...models import Books


# View Details of Book by ID
@book.route('/view/<string:id>')
def viewBook(id):
    # Create MySQLCursor
    
    book = Books.query.get(id)

    if book is not None:
        return render_template('book/view_book.html', book=book)
    else:
        msg = 'This book Does Not Exist'
        return render_template('book/view_book.html', warning=msg)