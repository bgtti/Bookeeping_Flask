from flask import current_app
from app.extensions import db
# from app.models.user import Blog_User
from app.dummie_data import expenses_data

# ADMIN_NAME = "Super Admin"
# ADMIN_EMAIL = "super@admin"
# ADMIN_PW = "admin123"


# def create_admin_acct():
    # Check if a super_admin exists in the database, if not, add it as well as the default author and default user:
    # Note that these three users will not count towards the number of users using the blog (in the blog stats)
    # super_admin_exists = Blog_User.query.get(1)
    # if not super_admin_exists:
    #     the_super_admin = Blog_User(
    #         name=ADMIN_NAME, email=ADMIN_EMAIL, password=hash_pw(ADMIN_PW), type="super_admin", picture=ADMIN_PICTURE)
    #     the_default_author = Blog_User(name=DEFAULT_AUTHOR_NAME, email=DEFAULT_AUTHOR_EMAIL, password=hash_pw(DEFAULT_AUTHOR_PW),
    #                                    type="author", about=DEFAULT_AUTHOR_ABOUT, picture=DEFAULT_AUTHOR_PICTURE)
    #     the_default_user = Blog_User(name=DEFAULT_USER_NAME, email=DEFAULT_USER_EMAIL, password=hash_pw(DEFAULT_USER_PW),
    #                                  type="user", about=DEFAULT_USER_ABOUT, picture=DEFAULT_USER_PICTURE)
    #     db.session.add(the_super_admin)
    #     db.session.add(the_default_author)
    #     db.session.add(the_default_user)
    #     db.session.commit()
