from sqlalchemy import Column, String, Integer, Float, DateTime, TIMESTAMP, text, ForeignKey
from orm_interface.base import Base

class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String)
    body = Column(String)
    created_on = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    category = Column(String)

    def __init__(self, user_id, title, body, created_on, category, id=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.created_on = created_on
        self.category = category