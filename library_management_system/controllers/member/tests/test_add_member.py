import unittest
from library_management_system import db, start_app
from library_management_system.models import Members
from time import sleep


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

    def test_add_member_some_time_after_models_are_evaluated(self):
        # Previously, the created_on time was set to whatever datetime
        # the models were evaluated for the first time

        # So, once the app starts, all of the members would have same datetime
        # even if they are created some time apart

        # This test case validates whether all the members are not having same `created_on`

        with self.app.application.app_context():
            new_member_1 = {"name": "Test", "email": "test@flask.com", "outstanding_debt": 0, "amount_spent": 0}

            response = self.app.post("/member/add", data=new_member_1, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Assert that the member was added to the database
            member1: Members = db.session.query(Members).filter(Members.email == new_member_1['email']).one()

            self.assertIsNotNone(member1)
            self.assertEqual(member1.name, new_member_1["name"])

            # Sleep for 3 seconds so members are created >=3 seconds apart
            sleep(5)

            new_member_2 = {"name": "Test2", "email": "test2@flask.com", "outstanding_debt": 0, "amount_spent": 0}

            response = self.app.post("/member/add", data=new_member_2, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Assert that the member was added to the database
            member2: Members = db.session.query(Members).filter(Members.email == new_member_2['email']).one()

            self.assertIsNotNone(member2)
            self.assertEqual(member2.name, new_member_2["name"])

            # Assert if created on time for both members is different
            self.assertNotEqual(member1.created_on, member2.created_on)
