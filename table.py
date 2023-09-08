from sqlalchemy import Column, Integer, VARCHAR, DateTime, SmallInteger, BIGINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Votes(Base):
    __tablename__ = 'votes'
    voter_id = Column(BIGINT, primary_key=True)
    ballot = Column(Integer)