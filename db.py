import logging

import sqlalchemy as db
from pymysql import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import MYSQL_URL

base = declarative_base()


def connection_mariaDB():
    try:
        return db.create_engine(MYSQL_URL)
    except OperationalError:
        raise



def generate_metadata():
    try:
        base.metadata.create_all(bind=connection_mariaDB())
    except Exception as e:
        logging.error(e)
        raise


def generate_session():
    try:
        session = sessionmaker()
        session.configure(bind=connection_mariaDB())
        return session()
    except Exception as e:
        logging.error(e)
        raise


class Images(base):
    __tablename__ = "images"
    name = db.Column(db.String(255), primary_key=True)
    old_key = db.Column(db.String(255))
    new_key = db.Column(db.String(255))
