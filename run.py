"""Routes for the course resource.
"""

"""
-------------------------------------------------------------------------
Challenge general notes:
-------------------------------------------------------------------------

1. Bonus points for returning sensible HTTP codes from the API routes
2. Bonus points for efficient code (e.g. title search)
"""

from flask import Flask
from models.database import db
import data


def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    db_name = 'db.sqlite3'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        # # Import the API routes
        from routes import course
        from models.course import Course
        db.create_all()  # Create sql tables for our data models

        print("Loading data", end=" ")
        data.load_data()
        print("... done")

        return app

app = init_app()

# Required because app is imported in other modules
if __name__== '__main__':
    app.run()
