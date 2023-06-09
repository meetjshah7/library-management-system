from wtforms import EmailField, Form, StringField, validators


class AddMember(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    email = EmailField("Email", [validators.Length(min=6, max=50)])
