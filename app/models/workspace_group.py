from app.extensions import db
from flask_login import UserMixin
from uuid import uuid4

# IN THIS FILE: Workspaces' Group DB Model

# uuid generation
def get_uuid():
    return uuid4().hex

# One workspace can have many groups. A group belongs to one workspace.
class Group(UserMixin, db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(30), nullable=False)
    _description = db.Column(db.String(100), nullable=True)
    _code = db.Column(db.String(10), nullable=True)
    _workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    subgroups = db.relationship('Subgroup', backref='group', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, description, code, workspace_id, ** kwargs):
        self._name = name
        self._description = description
        self._code = code
        self._workspace_id = workspace_id

    @property
    def uuid(self):
        return self._uuid
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def code(self):
        return self._code
    
    @property
    def  workspace_id(self):
        return self._workspace_id