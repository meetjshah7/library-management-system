from flask import flash, redirect, render_template, request, url_for

from library_management_system import db
from library_management_system.controllers.member.add_edit_form import \
    AddMember

from ...models import Members
from . import members


@members.route("/add", methods=["GET", "POST"])
def add_member():
    """
    Add a new member.

    Returns:
        Redirects to the route for displaying all members.
    """

    form: AddMember = AddMember(request.form)

    if request.method == "POST" and form.validate():
        try:
            name = form.name.data
            email = form.email.data

            new = {"name": name, "email": email, "outstanding_debt": 0, "amount_spent": 0}

            new_member = Members(new)
            db.session.add(new_member)
            db.session.commit()

            flash("Wohoo! New Member Added Successfully", "success")
            return redirect(url_for("members.all_members"))
        except Exception as e:
            flash(f"Some error occurred {e}", "danger")
            return render_template("member/add_member.html", form=form)

    return render_template("member/add_member.html", form=form)
