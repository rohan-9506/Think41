from app import db
from datetime import datetime

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_str_id = db.Column(db.String, unique=True, nullable=False)
    question = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

    options = db.relationship('PollOption', backref='poll', lazy=True)

class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_str_id = db.Column(db.String, unique=True, nullable=False)
    text = db.Column(db.String, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

class VoteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    poll_id = db.Column(db.Integer, nullable=False)
    option_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'poll_id', name='_user_poll_uc'),)
