<<<<<<< HEAD
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    group = db.relationship('UserGroup', back_populates='user')
    role = db.relationship('UserRole', back_populates='user')
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Group(db.Model):
    """
    Create a Group table
    """

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(200))
    user = db.relationship('UserGroup', back_populates='group')
    access_dashboard = db.Column(db.Boolean, default=False)
    access_api = db.Column(db.Boolean, default=False)
    access_setting = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Group: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    user = db.relationship('UserRole', back_populates='role')
    permission_create = db.Column(db.Boolean, default=False)
    permission_update = db.Column(db.Boolean, default=False)
    permission_delete = db.Column(db.Boolean, default=False)
    permission_read = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Setting(db.Model):
    """
    Create Settings configuration model
    """
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Settings: {}>'.format(self.name)


class UserGroup(db.Model):
    """
    This is middle table for user and group table
    """
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    user = db.relationship('User', primaryjoin=user_id == User.id)
    group = db.relationship('Group', primaryjoin=group_id == Group.id)


class UserRole(db.Model):
    """
    This is middle table for user and role table
    """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    user = db.relationship('User', primaryjoin=user_id == User.id)
    role = db.relationship('Role', primaryjoin=role_id == Role.id)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
=======
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    group = db.relationship('UserGroup', back_populates='user')
    role = db.relationship('UserRole', back_populates='user')
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Group(db.Model):
    """
    Create a Group table
    """

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(200))
    user = db.relationship('UserGroup', back_populates='group')
    access_dashboard = db.Column(db.Boolean, default=False)
    access_api = db.Column(db.Boolean, default=False)
    access_setting = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Group: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    user = db.relationship('UserRole', back_populates='role')
    permission_create = db.Column(db.Boolean, default=False)
    permission_update = db.Column(db.Boolean, default=False)
    permission_delete = db.Column(db.Boolean, default=False)
    permission_read = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Setting(db.Model):
    """
    Create Settings configuration model
    """
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Settings: {}>'.format(self.name)


class UserGroup(db.Model):
    """
    This is middle table for user and group table
    """
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    user = db.relationship('User', primaryjoin=user_id == User.id)
    group = db.relationship('Group', primaryjoin=group_id == Group.id)


class UserRole(db.Model):
    """
    This is middle table for user and role table
    """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    user = db.relationship('User', primaryjoin=user_id == User.id)
    role = db.relationship('Role', primaryjoin=role_id == Role.id)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
