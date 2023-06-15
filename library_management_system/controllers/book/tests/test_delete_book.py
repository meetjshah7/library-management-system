import unittest

from library_management_system import db, start_app
from library_management_system.models import Books


class DeleteBookTestCase(unittest.TestCase):
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

    def test_delete_book(self):
        with self.app.application.app_context():
            data = {
                "bookID": "123",
                "isbn": "1234567890",
                "isbn13": "1234567890123",
                "title": "Test Book",
                "quantity": 10,
                "authors": "John Doe",
                "average_rating": 4.5,
                "language_code": "en",
                "num_pages": 200,
                "ratings_count": 100,
                "text_reviews_count": 20,
                "publication_date": "01/01/2022",
                "publisher": "Test Publisher"
            }

            new_book = Books(data, 10)
            db.session.add(new_book)
            db.session.commit()

            # Assert that the book is present to the database
            book: Books = db.session.query(Books).filter(Books.book_id == data['bookID']).one()
            self.assertIsNotNone(book)
            self.assertEqual(book.title, data["title"])

            # Delete book
            delete_book_response = self.app.post(f"/book/delete/{book.id}", follow_redirects=True)
            self.assertEqual(delete_book_response.status_code, 200)

            # Assert that the book was deleted from the database
            book: Books = db.session.query(Books).filter(Books.book_id == data['bookID'])
            self.assertEqual(book.count(), 0)
