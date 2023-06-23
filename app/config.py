import os
# from dotenv import load_dotenv  # getting .env variables
# from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # needed for login with wtforms
    SQLALCHEMY_DATABASE_URI = 'sqlite:///admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
