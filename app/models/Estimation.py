import datetime
from app.db import db


class Estimation(db.Model):
    """User account model."""

    __tablename__ = "estimation"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'), nullable=False)
    estimation = db.Column("estimation", db.Text, nullable=False)
    rm = db.Column('rm', db.Float, nullable=False)
    lstat = db.Column('lstat', db.Float, nullable=False)
    ptratio = db.Column('ptratio', db.Float, nullable=False)
    created_at = db.Column("created_at", db.DateTime, default=datetime.datetime.utcnow)