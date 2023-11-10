from app.extensions import db
from flask_login import UserMixin
from uuid import uuid4

# IN THIS FILE: Workspaces' Tag DB Model

# uuid generation
def get_uuid():
    return uuid4().hex

# One workspace can have many tags. A tag belongs to one workspace.
class Tag(UserMixin, db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(30), nullable=False)
    _colour = db.Column(db.String(7), nullable=False, default="#595d66")
    _workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))

    def __init__(self, name, colour, workspace_id, ** kwargs):
        self._name = name
        self._colour = colour
        self._workspace_id = workspace_id

    @property
    def uuid(self):
        return self._uuid
    
    @property
    def name(self):
        return self._name
    
    @property
    def colour(self):
        return self._colour
    
    @property
    def  workspace_id(self):
        return self._workspace_id