from flask import flash, redirect, url_for
from . import members
from ...models import Members


@members.route("/delete/<string:id>", methods=["POST"])
def delete_member(id):
    """
    Delete a member.

    Parameters:
        id (str): The ID of the member to be deleted.

    Returns:
        Redirects to the route for displaying all members.
    """

    try:
        Members.query.filter(Members.id == id).delete()
    except Exception as e:
        print(e)
        flash(f"Member could not be deleted. Reason {e}", "danger")
        return redirect(url_for("members.all_members"))

    flash("Member Deleted", "success")
    return redirect(url_for("members.all_members"))
