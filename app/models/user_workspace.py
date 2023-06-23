from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

# User and Workspace Models
# The user who creates the Workspace is the owner
# The owner may share the workspace with other users, giving some user access to the workspace

uw_relationship = db.Table("uw_relationship",
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('workspace_id', db.Integer, db.ForeignKey('workspaces.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(200), nullable=False)
    _email = db.Column(db.String(200), nullable=False, unique=True)
    _password = db.Column(db.String(200), nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owned_workspaces = db.relationship('Workspace', 
                                        backref='owner', 
                                        cascade='all,delete', 
                                        passive_deletes='all') #one-to-many (many workspaces can be owned by one user)
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
    
    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    @property
    def password(self):
        return self._password


# new user: 
# new_user = User(email='example@example.com', name='John Doe', password='password123')
# db.session.add(new_user)
# db.session.commit()


class Workspace(UserMixin, db.Model):
    __tablename__ = "workspace"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(200), nullable=False)
    _currency = db.Column(db.String(10), default="USD")
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))

    def __init__(self, name, owner_id, ** kwargs):
        self._name = name
        self._created_at = datetime.utcnow()
        self.owner_id = owner_id

    def __repr__(self):
        return f"<Workspace: {self.id} {self._name} owned by {self.owner_id}>"

    @property
    def name(self):
        return self._name

    @property
    def currency(self):
        return self._currency
    

# many-to-many relationship add:
# userX.workspaces.append(workspaceY)
# db.session.add(userX)

# many-to-many relationship list workspaces userX has access to:
# userX.workspaces.all()
# many-to-many relationship list users with access to workspaceY:
# workspaceY.users.all()
# end many-to-many relationship:
# userX.workspaces.remove(workspaceY)

