from typing import Optional
import unittest
from datetime import datetime, timedelta

from werkzeug.datastructures import MultiDict

from library_management_system import db, start_app
from library_management_system.controllers.transactions.return_book import \
    ReturnBook
from library_management_system.models import Books, Members, Transactions


class ReturnBookTestCase(unittest.TestCase):
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

    def test_return_book_valid_data(self):
        with self.app.application.app_context():
            # Add initial data
            member = Members(
                {
                    "name": "Test",
                    "email": "abc@xyz.com",
                    "outstanding_debt": 0,
                    "amount_spent": 0
                }
            )
            book = Books(
                {
                    "bookID": 1231,
                    "isbn": 1234567890,
                    "isbn13": 1234567890000,
                    "title": "Test",
                    "quantity": 5,
                    "authors": "Test",
                    "average_rating": 3,
                    "language_code": "python",
                    "num_pages": 123,
                    "ratings_count": 322,
                    "text_reviews_count": 10,
                    "publication_date": "05/20/2000",
                    "publisher": "test"
                },
                5
            )
            db.session.add_all([member, book])
            db.session.commit()

            transaction = Transactions(member_id=member.id, book_id=book.id, per_day_rent=10)
            # Marking the books as issued
            book.issued = 1

            db.session.add(transaction)
            db.session.commit()

            # Create a valid form
            form_data = MultiDict({"amount_paid": 10})
            form = ReturnBook(formdata=form_data)

            # Call return_book POST API
            response = self.app.post(
                f"/transaction/return_book/{transaction.id}",
                data=form.data,
                follow_redirects=True,
            )

            # Assert if the transaction was successfully processed
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Book Returned", response.data)

            # Assert if the transaction and member records were updated correctly
            updated_transaction: Optional[Transactions] = db.session.get(Transactions, transaction.id)
            updated_member: Optional[Members] = db.session.get(Members, member.id)

            assert updated_transaction is not None
            self.assertIsNotNone(updated_transaction.returned_on)
            self.assertEqual(updated_transaction.amount_settled, 10)
            self.assertTrue(updated_transaction.book_returned)

            assert updated_member is not None
            self.assertEqual(updated_member.outstanding_debt, -10)
            self.assertEqual(updated_member.amount_spent, 10)

            # Asseert if the book record was updated correctly
            updated_book: Optional[Books] = db.session.get(Books, book.id)
            assert updated_book is not None
            self.assertEqual(updated_book.issued, 0)

    def test_return_book_violate_outstanding_debt(self):
        with self.app.application.app_context():
            # Add initial data
            member = Members(
                {
                    "name": "Test",
                    "email": "abc@xyz.com",
                    "outstanding_debt": 500,
                    "amount_spent": 0
                }
            )
            book = Books(
                {
                    "bookID": 1231,
                    "isbn": 1234567890,
                    "isbn13": 1234567890000,
                    "title": "Test",
                    "quantity": 5,
                    "authors": "Test",
                    "average_rating": 3,
                    "language_code": "python",
                    "num_pages": 123,
                    "ratings_count": 322,
                    "text_reviews_count": 10,
                    "publication_date": "05/20/2000",
                    "publisher": "test"
                },
                5
            )
            db.session.add_all([member, book])
            db.session.commit()

            transaction = Transactions(member_id=member.id, book_id=book.id, per_day_rent=10)
            db.session.add(transaction)
            db.session.commit()

            transaction.issued_on = datetime.now() - timedelta(days=2, hours=3)
            db.session.commit()

            # Create a form with amount_paid = 0
            form_data = MultiDict({"amount_paid": 10})
            form = ReturnBook(formdata=form_data)

            # Call return_book POST API
            response = self.app.post(
                f"/transaction/return_book/{transaction.id}",
                data=form.data,
                follow_redirects=True,
            )

            # Assert if the error message is displayed
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Outstanding Debt Cannot Exceed Rs.500", response.data)
