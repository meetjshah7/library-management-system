import unittest

from library_management_system import db, start_app
from library_management_system.models import Members


class DeleteMemberTestCase(unittest.TestCase):
    def setUp(self):
        app = start_app()[0]
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb"
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.application.app_context():
            db.session.remove()
            db.drop_all()

    def test_delete_member(self):
        with self.app.application.app_context():
            data = {"name": "Test", "email": "test@flask.com", "outstanding_debt": 0, "amount_spent": 0}
            new_member = Members(data)
            db.session.add(new_member)
            db.session.commit()

            # Assert that the member is present to the database
            member: Members = db.session.query(Members).filter(Members.email == data['email']).one()
            self.assertIsNotNone(member)
            self.assertEqual(member.name, data["name"])

            # Delete member
            delete_member_response = self.app.post(f"/member/delete/{member.id}", follow_redirects=True)
            self.assertEqual(delete_member_response.status_code, 200)

            # Assert that the member was deleted from the database
            member: Members = db.session.query(Members).filter(Members.email == data['email'])
            self.assertEqual(member.count(), 0)
