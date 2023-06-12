from flask import render_template, flash, redirect, url_for, request
from library_management_system import db
from library_management_system.controllers.member.add_edit_form import AddMember
from . import members
from ...models import Members


@members.route("/add", methods=["GET", "POST"])
def add_member():
    """
    Add a new member.

    Returns:
        Redirects to the route for displaying all members.
    """

    form: AddMember = AddMember(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data

        new = {"name": name, "email": email, "outstanding_debt": 0, "amount_spent": 0}

        new_member = Members(new)
        db.session.add(new_member)
        db.session.commit()

        flash("Wohoo! New Member Added Successfully", "success")

        return redirect(url_for("members.all_members"))

    return render_template("member/add_member.html", form=form)
