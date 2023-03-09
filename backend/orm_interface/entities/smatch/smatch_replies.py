from sqlalchemy import Column, String, Integer, Float, DateTime, TIMESTAMP, text, ForeignKey
from orm_interface.base import Base

class Smatch_Reply(Base):
    __tablename__ = "smatch_replies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    thread_id = Column(Integer, ForeignKey('smatch_threads.id'))
    body = Column(String)
    created_on = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(self, user_id, thread_id, body, created_on, id=None):
        self.id = id
        self.user_id = user_id
        self.thread_id = thread_id
        self.body = body
        self.created_on = created_on