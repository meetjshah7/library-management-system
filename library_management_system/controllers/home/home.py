from flask import Blueprint, render_template

home = Blueprint("home", __name__)


@home.route("/")
def home_page():
    """
    Render the home page.

    Returns:
        Renders the 'home' template.
    """

    return render_template("home.html", title="Home")
