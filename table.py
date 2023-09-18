from sqlalchemy import Column, Integer, VARCHAR, DateTime, SmallInteger, BIGINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Votes(Base):
    __tablename__ = 'votes'
    voter_id = Column(BIGINT, primary_key=True)
    ballot = Column(Integer)


class BC_Votes(Base):
    __tablename__ = 'bc_votes'
    id = Column(BIGINT, primary_key=True)
    ballot_data = Column(VARCHAR)