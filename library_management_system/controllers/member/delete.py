from flask import flash, redirect, url_for
from . import members
from library_management_system import db
from ...models import Members


@members.route('/delete/<string:id>', methods=['POST'])
def delete_member(id):
    try:
        db.session.query(Members).filter(Members.id==id).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        
        flash("Member could not be deleted", "danger")
        flash(str(e), "danger")

        return redirect(url_for('members.all_members'))

    flash("Member Deleted", "success")

    return redirect(url_for('members.all_members'))