"""Routines associated with the application data.
"""

courses = {}

def load_data():
    """Load the data from the json file.
    """
    import json, os
    from models.database import db
    from models.course import Course
    from datetime import datetime as dt

    courses_qs = db.session.query(Course).all()
    if courses_qs:
        print('... Courses already exists', end=" ")
        return True

    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "json", "course.json")

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for dct in data:
            dct['date_updated'] = dt.strptime(dct['date_updated'], "%Y-%m-%d %H:%M:%S")
            dct['date_created'] = dt.strptime(dct['date_created'], "%Y-%m-%d %H:%M:%S")

            course_obj = Course(**dct)
            db.session.add(course_obj)
            db.session.commit()


