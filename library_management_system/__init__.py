
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_NAME = "bookshelf1.db"

def start_app():
    app = Flask(__name__)

    app.secret_key = 'IamSecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app=app)

    from .controllers.home.home import home
    app.register_blueprint(home)
    
    from .controllers.member import members
    app.register_blueprint(members)
    
    from .controllers.book import book
    app.register_blueprint(book)
    
    from .controllers.transactions import transaction
    app.register_blueprint(transaction)

    from .controllers.report import report
    app.register_blueprint(report)

    
    print(app.url_map)

    return app, db