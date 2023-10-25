from flask import current_app
from app.extensions import db, flask_bcrypt
from app.models.user_and_workspace import User, Workspace
from app.dummie_data import expenses_data
from app.account.salt import generate_salt

# Creates an admin account
# At this point the admin account is just like any other account

# Data for Admin Account creation:
ADMIN_NAME = "Super Admin"
ADMIN_EMAIL = "super@admin"
ADMIN_PW = "admin123"

def create_admin_acct():
    # Check if SUper Admin exists in the database, if not, add it:
    super_admin_exists = User.query.get(1)
    if not super_admin_exists:
        # create super admin
        salt = generate_salt()
        salted_pw = salt + ADMIN_PW
        hashed_password = flask_bcrypt.generate_password_hash(salted_pw ).decode('utf-8')
        the_super_admin = User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password, salt=salt)
        db.session.add(the_super_admin)
        db.session.commit()
        #create admin workspace
        name = "My Admin Work Space"
        currency = "CHF"
        super_admin_workspace = Workspace(name=name, abbreviation='AD', currency=currency, owner_id=the_super_admin.id)
        db.session.add(super_admin_workspace)
        db.session.commit() 