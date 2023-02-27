from sqlalchemy import Column, String, Integer, Float, DateTime, TIMESTAMP, text
from orm_interface.base import Base

class ReplieOld(Base):
    __tablename__ = "replies_old"

    id = Column(Integer, primary_key=True)
    reply_id = Column(Integer)
    thread_id = Column(Integer)
    body = Column(String)
    created_on = Column(String)
    username = Column(String)

    def __init__(self, id, reply_id, thread_id, body, created_on, username):
        self.id = id
        self.reply_id = reply_id
        self.thread_id = thread_id
        self.body = body
        self.created_on = created_on
        self.username = username