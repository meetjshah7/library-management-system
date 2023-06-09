from flask import render_template

from ...models import Members
from . import members


@members.route("/view/<string:id>", methods=["GET"])
def view_member(id):
    """
    View the details of a member.

    Parameters:
        id (str): The ID of the member to be viewed.

    Returns:
        Renders the 'Member Details' template with the member details.
        If the member does not exist, it renders the template with a warning message.
    """

    member = Members.query.get(id)

    if member is not None:
        return render_template("member/view_member.html", member=member)
    else:
        msg = "This Member Does Not Exist"
        return render_template("member/view_member.html", warning=msg)
