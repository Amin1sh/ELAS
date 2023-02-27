from sqlalchemy import Column, String, Integer, Float
from orm_interface.base import Base

class MatchedTerm(Base):
    __tablename__ = "matched_terms"

    id = Column(Integer, primary_key=True)
    term = Column(String)
    count = Column(Integer)

    def __init__(self, id, term, count):
        self.id = id
        self.term = term
        self.count = count