import unittest
from library_management_system import start_app, db
from library_management_system.models import Books


class TestBookImport(unittest.TestCase):
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

    def test_import_books(self):
        with self.app.application.app_context():
            form_data = {
                'no_of_books': 20,
                'quantity_per_book': 1
            }

            # Call import POST API
            response = self.app.post('/book/import', data=form_data, follow_redirects=True)

            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)

            # Assert that the flash message
            self.assertIn(b"20/20 books have been imported", response.data)

            # Assert that the 20 books are imported
            books = Books.query.all()
            self.assertEqual(len(books), 20)
