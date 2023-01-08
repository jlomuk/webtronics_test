import sqlalchemy as sq
from sqlalchemy import ForeignKey, DateTime, func

meta = sq.MetaData()

post = sq.Table(
    'post',
    meta,
    sq.Column('id', sq.Integer, primary_key=True),
    sq.Column('title', sq.String, nullable=False),
    sq.Column('body', sq.String, nullable=False),
    sq.Column('user_id', sq.Integer, index=True, nullable=False),
    sq.Column('email', sq.String, nullable=False, index=True),
    sq.Column('created_date', DateTime(timezone=True), server_default=func.now())
)

reaction = sq.Table(
    'reaction',
    meta,
    sq.Column('id', sq.Integer, primary_key=True),
    sq.Column('like', sq.Boolean, nullable=True),
    sq.Column("post_id", sq.Integer, ForeignKey("post.id", ondelete='CASCADE'), nullable=False),
    sq.Column("user_id", sq.Integer, nullable=False, index=True),
)
