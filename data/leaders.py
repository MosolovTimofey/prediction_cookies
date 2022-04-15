import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Leaders(SqlAlchemyBase):
    __tablename__ = 'leaders'

    place = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.name"))

    user = orm.relation('User')
