from flask import current_app
from app.extensions import db, flask_bcrypt
from app.models.user_workspace import User, Workspace
from app.dummie_data import expenses_data

ADMIN_NAME = "Super Admin"
ADMIN_EMAIL = "super@admin"
ADMIN_PW = "admin123"


def create_admin_acct():
    # Check if SUper Admin exists in the database, if not, add it:
    super_admin_exists = User.query.get(1)
    if not super_admin_exists:
        # create super admin
        hashed_password = flask_bcrypt.generate_password_hash(ADMIN_PW).decode('utf-8')
        the_super_admin = User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password)
        db.session.add(the_super_admin)
        db.session.commit()
        #create admin workspace
        name = "My Admin Work Space"
        currency = "CHF"
        super_admin_workspace = Workspace(name=name, abbreviation='ADM', currency=currency, owner_id=the_super_admin.id)
        db.session.add(super_admin_workspace)
        db.session.commit() 