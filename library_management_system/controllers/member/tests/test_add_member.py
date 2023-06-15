import unittest

from library_management_system import db, start_app
from library_management_system.models import Members


class AddMemberTestCase(unittest.TestCase):
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

    def test_add_member(self):
        with self.app.application.app_context():
            new_data = {"name": "Test", "email": "test@flask.com", "outstanding_debt": 0, "amount_spent": 0}

            response = self.app.post("/member/add", data=new_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Assert that the member was added to the database
            member: Members = db.session.query(Members).filter(Members.email == new_data['email']).one()
            self.assertIsNotNone(member)
            self.assertEqual(member.name, new_data["name"])
