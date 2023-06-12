from flask import Blueprint


report = Blueprint("reports", __name__, url_prefix='/report')


from . import reports