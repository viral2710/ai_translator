import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TranslationTask(Base):
    __tablename__ = "translation_tasks"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    languages = sqlalchemy.Column(sqlalchemy.JSON, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, default="in progress", nullable=False)
    translations = sqlalchemy.Column(sqlalchemy.JSON, default={})
