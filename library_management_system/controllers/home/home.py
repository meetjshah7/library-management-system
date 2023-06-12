from flask import Blueprint, render_template

home = Blueprint("home", __name__)


@home.route("/")
def home_page():
    """
    Render the home page.

    Returns:
        Renders the 'home.html' template with the title set to 'Home'.
    """

    return render_template("home.html", title="Home")
