from sqlalchemy import Column, String, Integer, Float, DateTime, TIMESTAMP, text, ForeignKey
from orm_interface.base import Base

class Smatch_History(Base):
    __tablename__ = "smatch_histories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    topic = Column(String)
    result = Column(String)
    created_on = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(self, user_id, topic, result, created_on=None, id=None):
        self.id = id
        self.user_id = user_id
        self.result = result
        self.topic = topic
        self.created_on = created_on