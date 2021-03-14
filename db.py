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


class Pictures(base):
    __tablename__ = "Pictures"
    old_route = db.Column(db.String(255), primary_key=True)
    new_route = db.Column(db.String(255))
