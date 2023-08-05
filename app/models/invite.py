from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4
from .user_workspace import Workspace, User

def get_uuid():
    return uuid4().hex

# used for sharing Workspace or transfer of Workspace ownership
# when invite is accepted or cancelled, it should be deleted
# while invite exists, status is pending

INVITE_TYPES = ['give_access', 'ownership_transfer']

class Invite(UserMixin, db.Model):
    __tablename__ = "invites"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _type = db.Column(db.String(200), nullable=False, default=INVITE_TYPES[0])
    _title = db.Column(db.String(200), nullable=False, default='You have been invited to join a Work Space')
    _text = db.Column(db.String(200), default='')
    _email_of_invited = db.Column(db.String(345), nullable=False)
    _user_who_sent_invite = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _workspace_in_question = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email_of_invited, user_who_sent_invite, workspace_in_question, ** kwargs):
        self._email_of_invited = email_of_invited
        self._user_who_sent_invite = user_who_sent_invite
        self._workspace_in_question = workspace_in_question

    def __repr__(self):
        return f"<Invite: {self.id} type {self._type} sent to {self._email_of_invited} by {self._user_who_sent_invite }>"
    
    @property
    def type (self):
        return self._type 
    @property
    def title (self):
        return self._title 
    @property
    def text (self):
        return self._text 
    @property
    def email_of_invited (self):
        return self._email_of_invited 
    @property
    def workspace_in_question (self):
        return self._workspace_in_question 