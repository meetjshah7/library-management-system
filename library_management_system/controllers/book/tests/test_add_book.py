import unittest

from library_management_system import db, start_app
from library_management_system.models import Books
from time import sleep

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

    def test_add_book_some_time_after_models_are_evaluated(self):
        # Previously, the added time was set to whatever datetime
        # the models were evaluated for the first time

        # So, once the app starts, all of the books would have same datetime
        # even if they are created some time apart

        # This test case validates whether all the books are not having same `added`

        with self.app.application.app_context():
            new_book_1 = {
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

            response = self.app.post("/book/add", data=new_book_1, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Assert that the book1 was added to the database
            book1: Books = db.session.query(Books).filter(Books.book_id == new_book_1['book_id']).one()
            self.assertIsNotNone(book1)
            self.assertEqual(book1.title, new_book_1["title"])

            # Sleep for 3 seconds so books are created >=3 seconds apart
            sleep(5)

            new_book_2 = {
                "book_id": "1234",
                "isbn": "0987654321",
                "isbn13": "1231234567890",
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

            response = self.app.post("/book/add", data=new_book_2, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Assert that the book2 was added to the database
            book2: Books = db.session.query(Books).filter(Books.book_id == new_book_2['book_id']).one()
            self.assertIsNotNone(book2)
            self.assertEqual(book2.title, new_book_2["title"])

           # Assert if `added`` time for both books is different
            self.assertNotEqual(book1.added, book2.added)
