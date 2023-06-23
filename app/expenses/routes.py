from flask import Blueprint
# from app.extensions import db


expenses = Blueprint('expenses', __name__)

@expenses.route("/")
def test():
    return '<h1>Hello</>'