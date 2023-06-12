from flask import render_template
from . import members
from ...models import Members


@members.route('/view/<string:id>', methods=['GET'])
def viewMember(id):
    
    member = Members.query.get(id)

    if member is not None:
        return render_template('member/view_member.html', member=member)
    else:
        msg = 'This Member Does Not Exist'
        return render_template('member/view_member.html', warning=msg)