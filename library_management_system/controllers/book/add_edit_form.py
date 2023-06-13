from wtforms import Form, validators, StringField, FloatField, IntegerField, DateField


class AddBook(Form):
    book_id = StringField("Book ID", [validators.Length(min=1, max=11)])
    title = StringField("Title", [validators.Length(min=2, max=255)])
    author = StringField("Author(s)", [validators.Length(min=2, max=255)])
    average_rating = FloatField(
        "Average Rating", [validators.NumberRange(min=0, max=5)]
    )
    isbn = StringField("ISBN", [validators.Length(min=10, max=10)])
    isbn13 = StringField("ISBN13", [validators.Length(min=13, max=13)])
    language_code = StringField("Language", [validators.Length(min=1, max=10)])
    num_pages = IntegerField("No. of Pages", [validators.NumberRange(min=1)])
    ratings_count = IntegerField("No. of Ratings", [validators.NumberRange(min=0)])
    text_reviews_count = IntegerField(
        "No. of Text Reviews", [validators.NumberRange(min=0)]
    )
    publication_date = DateField("Publication Date", [validators.InputRequired()])
    publisher = StringField("Publisher", [validators.Length(min=2, max=255)])
    quantity = IntegerField("Total No. of Copies", [validators.NumberRange(min=1)])
