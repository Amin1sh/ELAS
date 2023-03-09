from sqlalchemy import Column, String, Integer, Float
from orm_interface.base import Base

class Smatch_MatchedTerm(Base):
    __tablename__ = "smatch_matched_terms"

    id = Column(Integer, primary_key=True)
    term = Column(String)
    count = Column(Integer)

    def __init__(self, term, count, id=None):
        self.id = id
        self.term = term
        self.count = count