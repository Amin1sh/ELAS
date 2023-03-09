from sqlalchemy import Column, String, Integer, Float, DateTime, TIMESTAMP, text
from orm_interface.base import Base

class Smatch_ThreadOld(Base):
    __tablename__ = "smatch_threads_old"

    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer)
    title = Column(String)
    body = Column(String)
    created_on = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    username = Column(String)

    def __init__(self, thread_id, title, body, created_on, username, id=None):
        self.id = id
        self.thread_id = thread_id
        self.title = title
        self.body = body
        self.created_on = created_on
        self.username = username