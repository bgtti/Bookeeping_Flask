from app.extensions import db
from sqlalchemy import event
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4
from .yy_mm_counter import YYMM_counter_expenses as YYMMCounter
from .user_and_workspace import Workspace

# uuid generation
def get_uuid():
    return uuid4().hex

# 
class Expense(UserMixin, db.Model):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _date = db.Column(db.DateTime, default=datetime.utcnow)
    _expense_nr_from_workspace_counter = db.Column(db.Integer, nullable=False, unique=True)
    _expense_nr_from_YYMM_counter = db.Column(db.Integer, nullable=False)
    _expense_nr_from_user = db.Column(db.String(50), nullable=True)
    _description = db.Column(db.String(100), nullable=False)
    _notes = db.Column(db.String(100), nullable=False)
    _amount = db.Column(db.Float, nullable=False) #amount in workspace currency
    _amount_in_foreign_currency = db.Column(db.Float, nullable=True) 
    _foreign_currency_used = db.Column(db.String(10), nullable=True)
    _workspace_id = db.Column(db.Integer, db.ForeignKey('workspace_id')) #important relationship
    # remember to write code that, if these the bellow is deleted, there is still some default.... like "None" or so
    _created_by = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=True) 
    _group_id = db.Column(db.Integer, db.ForeignKey('group_id'), nullable=True)
    _account_id = db.Column(db.Integer, db.ForeignKey('account_id'), nullable=True)
    _category_id = db.Column(db.Integer, db.ForeignKey('category_id'), nullable=True)

    def __init__(self, date, description, amount, workspace_id, ** kwargs):
        self._date = date
        self._description = description
        self._amount = amount
        self._workspace_id = workspace_id
        self._expense_nr_from_workspace_counter = 0  # Initialize with 0
        self._expense_nr_from_YYMM_counter = 0  # Initialize with 0

    @property
    def uuid(self):
        return self._uuid
    
    @property
    def date(self):
        return self._date
    
    @property
    def expense_nr_from_workspace_counter(self):
        return self._expense_nr_from_workspace_counter
    
    @property
    def expense_nr_from_YYMM_counter(self):
        return self._expense_nr_from_YYMM_counter
    
    @property
    def expense_nr_from_user(self):
        return self._expense_nr_from_user
    
    @property
    def description(self):
        return self._description
    
    @property
    def notes(self):
        return self._notes
    
    @property
    def amount(self):
        return self._amount
    
    @property
    def amount_in_foreign_currency(self):
        return self._amount_in_foreign_currency
    
    @property
    def  workspace_id(self):
        return self._workspace_id
    
    @property
    def  created_by(self):
        return self._created_by
    
    @property
    def  group_id(self):
        return self._group_id
    
    @property
    def  account_id(self):
        return self._account_id
    
    @property
    def  category_id(self):
        return self._category_id
    
    def create_expense(self, workspace_id, user_id, group_id, account_id, category_id):
        # Get the associated workspace
        workspace = Workspace.query.get(workspace_id)
        if workspace:
            # Increment the workspace's expense counter
            workspace._expenseCounter += 1

            # Set the expense number from the workspace counter
            self._expense_nr_from_workspace_counter = workspace._expenseCounter

            # Calculate year and month from _date
            year = self._date.year
            month = self._date.month

            # Check if a YYMMCounter record exists for this year and month
            yymm_counter = YYMMCounter.query.filter_by(year=year, month=month).first()
            if not yymm_counter:
                # Create a new YYMMCounter record if it doesn't exist
                yymm_counter = YYMMCounter(year=year, month=month, counter=0)
                db.session.add(yymm_counter)

            # Increment the YYMM counter
            yymm_counter.counter += 1

            # Set the expense number from the YYMMCounter
            self._expense_nr_from_YYMM_counter = yymm_counter.counter

            # Set other fields
            self._created_by = user_id
            self._group_id = group_id
            self._account_id = account_id
            self._category_id = category_id

            # Add and commit the expense to the database
            db.session.add(self)
            db.session.commit()

        return self