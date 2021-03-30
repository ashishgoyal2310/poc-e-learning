"""Routes for the course resource.
"""
import json

from flask import current_app as app
from flask import request, redirect, render_template, make_response, jsonify
from http import HTTPStatus
from datetime import datetime as dt
from sqlalchemy import or_, and_, not_
import data

from models.database import db
from models.course import Course


@app.route('/', methods=['GET'])
def home_view():
    """
    """
    return render_template(
        'home.html',
        title="Show Dashboard"
    )


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan on your data structure.

    -------------------------------------------------------------------------
    Curl Request: ## Get course by id
    -------------------------------------------------------------------------
    curl "http://localhost:5000/course/101"
    """
    # YOUR CODE HERE
    course_obj = db.session.query(Course).filter_by(id=id).first()

    if not course_obj:
        data = {"messge": "Course {} does not exist".format(id)}
        return make_response(jsonify(data), 404)

    data = {
        "data": course_obj.as_json()
    }
    return make_response(jsonify(data), 200)


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.

    -------------------------------------------------------------------------
    Curl Request: ## Get default page of courses
    -------------------------------------------------------------------------
    curl "http://localhost:5000/course?page-size=5"
    """
    # YOUR CODE HERE
    page_number = request.args.get('page-number', '1')
    page_number = int(page_number) if page_number.isdigit() else 1
    page_size = request.args.get('page-size', '10')
    page_size = int(page_size) if page_size.isdigit() else 10
    title_words = request.args.get('title-words', '')
    title_words = [word.strip() for word in title_words.split(',')] if title_words else []

    course_qs = db.session.query(Course)

    filter_group = []
    for search_word in title_words:
        filter_group.append(Course.title.like('%{}%'.format(search_word)))
        # filter_group.append(Course.description.like('%{}%'.format(search_word)))

    if filter_group:
        course_qs = course_qs.filter(or_(*filter_group))

    page_data = course_qs.paginate(page_number, page_size, error_out=False)

    data = {
        "data": [course_obj.as_json() for course_obj in page_data.items],
        "metadata": {
            "count": len(page_data.items),
            "page_count": page_data.pages,
            "page_number": page_number,
            "page_size": page_data.per_page,
            "record_count": course_qs.count()
        },
    }
    return make_response(jsonify(data), 200)


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields

    -------------------------------------------------------------------------
    Curl Request: ## Add course
    -------------------------------------------------------------------------
    curl -X "POST" "http://localhost:5000/course" \
        -H 'Content-Type: application/json' \
        -d $'{
    "description": "This is a brand new course",
    "discount_price": 5,
    "title": "Brand new course",
    "price": 25,
    "image_path": "images/some/path/foo.jpg",
    "on_discount": false
    }'
    """
    # YOUR CODE HERE
    try:
        request_data = json.loads(request.data)
    except Exception as exc:
        data = {"messge": "Invalid request data."}
        return make_response(jsonify(data), 400)

    course_kwargs = {
        'description': request_data.get('description', ''),
        'image_path': request_data.get('image_path', ''),
        'on_discount': True if request_data.get('on_discount', '') == 'true' else False,
        'discount_price': request_data.get('discount_price', ''),
        'price': request_data.get('price', ''),
        'title': request_data.get('title', ''),
        'date_created': dt.now(),
        'date_updated': dt.now(),
    }

    new_course = Course(**course_kwargs)
    try:
        db.session.add(new_course)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        data = {"messge": "Invalid request data. {}".format(exc)}
        return make_response(jsonify(data), 400)

    data = {"data": new_course.as_json()}
    return make_response(jsonify(data), 400)


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    -------------------------------------------------------------------------
    Challenge notes: ## Update course
    -------------------------------------------------------------------------
    curl -X "PUT" "http://localhost:5000/course/101" \
        -H 'Content-Type: application/json' \
        -d $'{
    "image_path": "images/some/path/foo.jpg",
    "discount_price": 5,
    "id": 101,
    "price": 25,
    "title": "Blah blah blah",
    "on_discount": false,
    "description": "New description"
    }'
    """
    # YOUR CODE HERE
    course_obj = db.session.query(Course).filter_by(id=id).first()
    if not course_obj:
        data = {"messge": "Course {} does not exist".format(id)}
        return make_response(jsonify(data), 404)

    try:
        request_data = json.loads(request.data)
    except Exception as exc:
        data = {"messge": "Invalid request data."}
        return make_response(jsonify(data), 400)

    for field in {'description','image_path','on_discount','discount_price','price','title'}:
        value = request_data.get(field, getattr(course_obj, field, ''))
        setattr(course_obj, field, value)
    course_obj.date_updated = dt.now()

    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        data = {"messge": "Invalid request data. {}".format(exc)}
        return make_response(jsonify(data), 400)

    data = {"data": course_obj.as_json()}
    return make_response(jsonify(data), 400)


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None

    -------------------------------------------------------------------------
    Curl Request: ## Delete course by id
    -------------------------------------------------------------------------
    curl -X "DELETE" "http://localhost:5000/course/101"
    """
    # YOUR CODE HERE
    course_obj = db.session.query(Course).filter_by(id=id).first()
    if not course_obj:
        data = {"messge": "Course {} does not exist".format(id)}
        return make_response(jsonify(data), 404)

    try:
        db.session.delete(course_obj)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        data = {"messge": "Invalid request data. {}".format(exc)}
        return make_response(jsonify(data), 400)

    data = {"message": "The specified course was deleted"}
    return make_response(jsonify(data), 400)