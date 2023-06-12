from flask import Blueprint


members = Blueprint("members", __name__, url_prefix='/member')


from . import list, get, add, delete, update  # noqa