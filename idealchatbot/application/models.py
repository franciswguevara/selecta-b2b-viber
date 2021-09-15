from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    fullname = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    outlet = db.Column(
        db.String(7),
        nullable=False,
        unique=True
    )
    address = db.Column(
        db.String(564),
        nullable=False,
        unique=False
    )
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False
    )
    status = db.Column(
        db.String(10),
        nullable=True,
        unique=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    cart = db.Column(
        db.,
        index=False,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return '<User {}>'.format(self.fullname)
