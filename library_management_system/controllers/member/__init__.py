from flask import Blueprint

members = Blueprint("members", __name__, url_prefix="/member")


from . import add, delete, get, members_list, update  # noqa
