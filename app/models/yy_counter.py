from app.extensions import db
from sqlalchemy import event
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4

# Expense number that tracks counters for each year and month
# Created from the Expense db model
class YYMM_counter_expenses(UserMixin, db.Model):
    __tablename__ = "YYMM_counter_expenses"
    id = db.Column(db.Integer, primary_key=True)
    _year = db.Column(db.Integer, nullable=False)
    _month = db.Column(db.Integer, nullable=False)
    _counter = db.Column(db.Integer, nullable=False, default=0)
    def __init__(self, year, month, counter):
        self._year = year
        self._month = month
        self._counter = counter
    @property
    def year(self):
        return self._year
    @property
    def month(self):
        return self._month
    @property
    def counter(self):
        return self._counter
    
# Expense number that tracks counters for each year
# Created from the Expense db model
class YY_counter_expenses(UserMixin, db.Model):
    __tablename__ = "YY_counter_expenses"
    id = db.Column(db.Integer, primary_key=True)
    _year = db.Column(db.Integer, nullable=False)
    _counter = db.Column(db.Integer, nullable=False, default=0)
    def __init__(self, year, counter):
        self._year = year
        self._counter = counter
    @property
    def year(self):
        return self._year
    @property
    def counter(self):
        return self._counter