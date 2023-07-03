from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import flask_bcrypt, db
from app.models.user_workspace import User
# from app.extensions import db


account = Blueprint('account', __name__)

@account.route("/register", methods=["POST"])
def registerUser():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if name == '' or email == None or len(email) > 200:
        return jsonify({'response':'no name or name not valid'})
    if email == '' or email == None or len(email) > 345:
        return jsonify({'response':'no email or email not valid'})
    if password == '' or password == None or len(password) > 70:
        return jsonify({'response':'no password or password not valid'})
    
    user_exists = User.query.filter_by(_email=email).first() is not None

    if user_exists:
        return jsonify({'response':'user already exists'}), 409

    hashed_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=email, expires_delta=timedelta(days=30))
    print(new_user)
    return jsonify({'response':'success', 'access_token':access_token})

@account.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    if email == '' or email == None or len(email) > 345:
        return jsonify({'response':'no email'})
    if password == '' or password == None or len(password) > 70:
        return jsonify({'response':'no password'})
    
    user = User.query.filter_by(_email=email).first()
    
    if user is None:
        return jsonify({'response':'unauthorized'}), 401
    
    if not flask_bcrypt.check_password_hash(user.password, password):
        return jsonify({'response':'unauthorized'}), 401
    
    access_token = create_access_token(identity=email, expires_delta=timedelta(days=30))
    return jsonify({'response':'success', 'access_token':access_token})

@account.route("/delete", methods=["POST"])
@jwt_required()  # Requires authentication
def deleteUser():
    current_user_email = get_jwt_identity()

    user = User.query.filter_by(_email=current_user_email).first()

    if not user:
        return jsonify({'response': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'response': 'User deleted successfully'})

# continuar  com: https://www.youtube.com/watch?v=8-W2O_R95Pk&t=793s
# min: 1:16