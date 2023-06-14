from flask import Blueprint

transaction = Blueprint("transaction", __name__, url_prefix="/transaction")


from . import issue_book, transactions_list, return_book  # noqa
