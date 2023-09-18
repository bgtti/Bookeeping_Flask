from app.extensions import db
from sqlalchemy import event
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4
from .workspace_settings_general import Group, Account

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
    _password = db.Column(db.String(70), nullable=False)
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
    
    def __init__(self, email, name, password, **kwargs):
        self._email = email
        self._name = name
        self._password = password
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
    
    # @property
    # def favorite_workspace(self):
    #     return self._favorite_workspace

event.listen(User, 'before_delete', User.before_delete)

class Workspace(UserMixin, db.Model):
    __tablename__ = "workspace"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(50), nullable=False)
    _abbreviation = db.Column(db.String(2), nullable=False, default='AB')
    _currency = db.Column(db.String(10), default="USD")
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    groups = db.relationship('Group', backref='workspace', lazy='dynamic', cascade='all, delete-orphan')
    accounts = db.relationship('Account', backref='workspace', lazy='dynamic', cascade='all, delete-orphan')

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

# many-to-many relationship add:
# userX.workspaces.append(workspaceY)
# db.session.add(userX)

# many-to-many relationship list workspaces userX has access to:
# userX.workspaces.all()
# many-to-many relationship list users with access to workspaceY:
# workspaceY.users.all()
# end many-to-many relationship:
# userX.workspaces.remove(workspaceY)

# used for sharing Workspace or transfer of Workspace ownership
# when invite is accepted or cancelled, it should be deleted
# while invite exists, status is pending
# INVITE_TYPES = ['give_access', 'ownership_transfer']

# class Invite(UserMixin, db.Model):
#     __tablename__ = "invites"
#     id = db.Column(db.Integer, primary_key=True)
#     _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
#     _type = db.Column(db.String(200), nullable=False, default=INVITE_TYPES[0])
#     _title = db.Column(db.String(200), nullable=False, default='You have been invited to join a Work Space')
#     _text = db.Column(db.String(200), default='')
#     _email_of_invited = db.Column(db.String(345), nullable=False)
#     _user_who_sent_invite = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     _workspace_in_question = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
#     _created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __init__(self, email_of_invited, user_who_sent_invite, workspace_in_question, ** kwargs):
#         self._email_of_invited = email_of_invited
#         self._user_who_sent_invite = user_who_sent_invite
#         self._workspace_in_question = workspace_in_question

#     def __repr__(self):
#         return f"<Invite: {self.id} type {self._type} sent to {self._email_of_invited} by {self._user_who_sent_invite }>"
    
#     @property
#     def type (self):
#         return self._type 
#     @property
#     def title (self):
#         return self._title 
#     @property
#     def text (self):
#         return self._text 
#     @property
#     def email_of_invited (self):
#         return self._email_of_invited 
#     @property
#     def workspace_in_question (self):
#         return self._workspace_in_question 

