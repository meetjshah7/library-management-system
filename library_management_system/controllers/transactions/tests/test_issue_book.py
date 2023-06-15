import unittest

from library_management_system import db, start_app
from library_management_system.models import Books, Members, Transactions


class IssueBookTestCase(unittest.TestCase):
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

    def test_issue_book(self):
        with self.app.application.app_context():
            # Add book and member
            book_data = {
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
            new_book = Books(book_data, 10)

            member_data = {"name": "Test", "email": "test@flask.com", "outstanding_debt": 0, "amount_spent": 0}
            new_member = Members(member_data)

            db.session.add_all([new_book, new_member])
            db.session.commit()

            data = {
                "book_id": "1",
                "member_id": "1",
                "per_day_rent": 5.0,
            }

            response = self.app.post("/transaction/issue_book", data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            transaction = db.session.query(Transactions).filter(
                Transactions.book_id == data["book_id"], Transactions.member_id == data["member_id"]
            ).one()
            self.assertIsNotNone(transaction)

    def test_issue_book_no_copies_available(self):
        with self.app.application.app_context():
            # Add book with 0 qty and member
            book_data = {
                "bookID": "123",
                "isbn": "1234567890",
                "isbn13": "1234567890123",
                "title": "Test Book",
                "quantity": 0,
                "authors": "John Doe",
                "average_rating": 4.5,
                "language_code": "en",
                "num_pages": 200,
                "ratings_count": 100,
                "text_reviews_count": 20,
                "publication_date": "01/01/2022",
                "publisher": "Test Publisher"
            }
            new_book = Books(book_data, 0)

            member_data = {"name": "Test", "email": "test@flask.com", "outstanding_debt": 0, "amount_spent": 0}
            new_member = Members(member_data)

            db.session.add_all([new_book, new_member])
            db.session.commit()
            
            data = {
                "book_id": "1",
                "member_id": "1",
                "per_day_rent": 5.0,
            }

            response = self.app.post("/transaction/issue_book", data=data)

            self.assertEqual(response.status_code, 200)

            error_message = "No copies of this book are availabe to be rented"
            self.assertIn(error_message, response.get_data(as_text=True))
