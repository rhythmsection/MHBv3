from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text

from sqlalchemy.orm import sessionmaker


ENGINE = None
Session = None

Base = declarative_base()

#Creating database to store song information.

class Fingerprint(Base):
    __tablename__ = "fingerprints"

    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = True)
    artist = Column(String, nullable = True)
    album = Column(String, nullable = True)
    fingerprint = Column(Text, nullable = True)

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///fingerprint_database.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

