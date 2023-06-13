from flask import flash, redirect, render_template, request, url_for

from library_management_system import db
from library_management_system.controllers.member.add_edit_form import \
    AddMember

from ...models import Members
from . import members


@members.route("/edit/<string:id>", methods=["GET", "POST"])
def edit_member(id):
    """
    Edit the details of a member.

    Parameters:
        id (str): The ID of the member to be edited.

    Returns:
        Redirects to the route for displaying all members after the member has been updated.

    """
    form: AddMember = AddMember(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data

        Members.query.filter(Members.id == id).update({"name": name, "email": email})
        db.session.commit()

        flash("Member Updated", "success")
        return redirect(url_for("members.all_members"))

    member = Members.query.get(id)
    return render_template("member/edit_member.html", form=form, member=member)
