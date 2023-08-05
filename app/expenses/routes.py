from flask import Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from app.extensions import db


expenses = Blueprint('expenses', __name__)

@expenses.route("/")
def test():
    return '<h1>Hello</>'


@expenses.route("/expenses")
@jwt_required()
def test2():
    return '<h1>Hello</>'