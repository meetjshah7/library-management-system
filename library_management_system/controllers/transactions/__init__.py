from flask import Blueprint


transaction = Blueprint("transaction", __name__, url_prefix="/transaction")


from . import list, issue_book, return_book  # noqa
