import sqlalchemy
from sqlalchemy import orm

from backend.data.db_session import SqlAlchemyBase


class JobsType(SqlAlchemyBase):
    __tablename__ = "jobs_type"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    jobs = orm.relationship("Jobs", back_populates="jobs_type")