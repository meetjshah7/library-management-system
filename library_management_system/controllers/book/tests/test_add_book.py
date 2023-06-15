import unittest

from library_management_system import db, start_app
from library_management_system.models import Books


class AddBookTestCase(unittest.TestCase):
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

    def test_add_book(self):
        with self.app.application.app_context():
            data = {
                "book_id": "123",
                "isbn": "1234567890",
                "isbn13": "1234567890123",
                "title": "Test Book",
                "quantity": 10,
                "author": "John Doe",
                "average_rating": 4.5,
                "language_code": "en",
                "num_pages": 200,
                "ratings_count": 100,
                "text_reviews_count": 20,
                "publication_date": "2022-01-01",
                "publisher": "Test Publisher"
            }

            response = self.app.post("/book/add", data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Assert that the book was added to the database
            book: Books = db.session.query(Books).filter(Books.book_id == data['book_id']).one()
            self.assertIsNotNone(book)
            self.assertEqual(book.title, data["title"])
