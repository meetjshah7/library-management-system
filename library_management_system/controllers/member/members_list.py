from flask import render_template, request

from library_management_system.models import Members

from . import members


@members.route("/list")
def all_members():
    """
    Display a list of all members.

    Returns:
        Renders the 'All Members' template with the paginated list of members
    """

    page = request.args.get("page", 1, type=int)
    members = Members.query.order_by(Members.id.asc()).paginate(page=page, per_page=5)
    is_empty = len(members.items) == 0
    return render_template(
        "member/members.html",
        title="Members",
        members=members,
        is_empty=is_empty,
        data=members.items,
    )
