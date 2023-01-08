import sqlalchemy as sq

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from databases import Database

from settings import settings

engine = create_engine(settings.POSTGRES_URL, echo=True)
metadata_obj = MetaData()

users = sq.Table(
    'users',
    metadata_obj,
    sq.Column('id', sq.Integer, primary_key=True),
    sq.Column('email', sq.String(), unique=True),
    sq.Column('password', sq.String())
)

database: Database = Database(settings.POSTGRES_URL)


def get_db():
    return database


def init_db():
    metadata_obj.create_all(engine)
