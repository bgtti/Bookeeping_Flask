from app.extensions import db
from sqlalchemy import event
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4
from app.models.workspace_group import Group
from app.models.workspace_account import Account
from app.models.expense_category import Expense_Category
from app.models.expense import Expense
# eventually import invites when this is implemented

# IN THIS FILE: User and Workspace DB Models

# uuid generation
def get_uuid():
    return uuid4().hex

# The user who creates the Workspace is the owner
# The owner may share the workspace with other users, giving some user access to the workspace

uw_relationship = db.Table("uw_relationship",
    db.Column('id', db.Integer, primary_key=True),  
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('workspace_id', db.Integer, db.ForeignKey('workspace.id'))
)

# note that before user is deleted, all owned workspaces will be deleted.
# owned_workspaces are those the user has created him/herself
# accessed_workspaces are those owned by others and shared with the user, so the user has access to them
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(200), nullable=False)
    _email = db.Column(db.String(345), nullable=False, unique=True)
    _password = db.Column(db.String(60), nullable=False)
    _salt = db.Column(db.String(8), nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    favorite_workspace = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    owned_workspaces = db.relationship('Workspace', 
                                        backref='the_owner', 
                                        cascade='all,delete', 
                                        foreign_keys="Workspace.owner_id") #one-to-many (many workspaces can be owned by one user)
    accessed_workspaces = db.relationship('Workspace', 
                                            secondary=uw_relationship,
                                            backref=db.backref('users', lazy='dynamic'),
                                            lazy='dynamic') #many-to-many relationship (many users can have access to many workspaces)
    
    def __init__(self, email, name, password, salt, **kwargs):
        self._email = email
        self._name = name
        self._password = password
        self._salt = salt
        self._created_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<User: {self.id} {self._name} {self._email}>"
    
    def delete_owned_workspaces(self):
        for workspace in self.owned_workspaces:
            db.session.delete(workspace)

    @staticmethod
    def before_delete(mapper, connection, target):
        target.delete_owned_workspaces()
    
    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    @property
    def password(self):
        return self._password
    
    @property
    def salt(self):
        return self._salt
    
    # @property
    # def favorite_workspace(self):
    #     return self._favorite_workspace

event.listen(User, 'before_delete', User.before_delete)

# These are the options for expense settings. If changed, make sure to review the Expense Model.
EXPENSE_NUMBER_DIGITS = [3,4,5] 
EXPENSE_NUMBER_FORMAT = ["YMN", "YN", "N"] #Where Y=year, M=month, N=number. Examples: 2023010001, 20230001, 0001. 
EXPENSE_NUMBER_YEAR_DIGITS = [2,4] 
EXPENSE_NUMBER_SEPARATOR = ["-", "/", ""] 

class Workspace(UserMixin, db.Model):
    __tablename__ = "workspace"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(50), nullable=False)
    _abbreviation = db.Column(db.String(2), nullable=False, default='AB')
    _currency = db.Column(db.String(10), default="USD")
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Expense numbering settings
    _expense_number_digits = db.Column(db.Integer, nullable=False, default=3)
    _expense_number_format = db.Column(db.String(3), nullable=False, default="YMN")
    _expense_number_start = db.Column(db.Integer, nullable=False, default=1)
    _expense_number_year_digits = db.Column(db.Integer, nullable=False, default=4)
    _expense_number_separator = db.Column(db.String(1), nullable=False, default="-")
    _expense_number_custom_prefix = db.Column(db.String(10), nullable=False, default="")
    _expense_counter = db.Column(db.Integer, nullable=False, default=0) #increases when an expense is added. Should never be changed manually: handled by the Expense model. This counter never resets.
    _expense_counter_custom_start = db.Column(db.Integer, nullable=False, default=0) #user-defined starting number for expense numbering. If added to _expense_nr_from_workspace_counter (in Expense) in FE, original counter can always be maintained and reverted back to.

    owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    groups = db.relationship('Group', backref='workspace', lazy='dynamic', cascade='all, delete-orphan')
    accounts = db.relationship('Account', backref='workspace', lazy='dynamic', cascade='all, delete-orphan')
    expense_categories = db.relationship('Expense_Category', backref='workspace', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='workspace', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, abbreviation, currency, owner_id, ** kwargs):
        self._name = name
        self._abbreviation = abbreviation
        self._created_at = datetime.utcnow()
        self._currency = currency
        self.owner_id = owner_id

    def __repr__(self):
        return f"<Workspace: {self.id} {self._name} owned by {self.owner_id}>"
    
    def get_groups(self):
        return self.groups.all()
    
    def get_accounts(self):
        return self.accounts.all()

    @property
    def uuid(self):
        return self._uuid
    
    @property
    def name(self):
        return self._name
    
    @property
    def abbreviation(self):
        return self._abbreviation

    @property
    def currency(self):
        return self._currency
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @abbreviation.setter
    def abbreviation(self, value):
        self._abbreviation = value
    
    @currency.setter
    def currency(self, value):
        self._currency = value


