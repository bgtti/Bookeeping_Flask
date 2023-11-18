from app.extensions import db
from flask_login import UserMixin
from uuid import uuid4

# IN THIS FILE: Group's Subgroup DB Model

# uuid generation
def get_uuid():
    return uuid4().hex

# One group can have many subgroups. A subgroup belongs to one group.
class Subgroup(UserMixin, db.Model):
    __tablename__ = "subgroup"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(30), nullable=False)
    _description = db.Column(db.String(100), nullable=True)
    _code = db.Column(db.String(10), nullable=True)
    _group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, name, description, code, group_id, ** kwargs):
        self._name = name
        self._description = description
        self._code = code
        self._group_id = group_id

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
    def  group_id(self):
        return self._group_id