import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()


def connection_mariaDB():
    return db.create_engine("mysql+pymysql://sketchUser:sketchPassword@localhost/sketch")


def generate_metadata():
    base.metadata.create_all(bind=connection_mariaDB())


def generate_session():
    Session = sessionmaker()
    Session.configure(bind=connection_mariaDB())
    return Session()


class Images(base):
    __tablename__ = "images"
    name = db.Column(db.String(255), primary_key=True)
    old_key = db.Column(db.String(255))
    new_key = db.Column(db.String(255))
