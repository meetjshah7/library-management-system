from flask import render_template, request
from . import transaction
from ...models import Transactions


@transaction.route("/list")
def all_transactions():
    page = request.args.get("page", 1, type=int)
    transactions = Transactions.query.order_by(Transactions.updated_on.desc()).paginate(
        page=page, per_page=5
    )
    return render_template(
        "transaction/transactions.html", title="Transactions", transactions=transactions
    )
