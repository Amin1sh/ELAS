from sqlalchemy import Column, String, Integer, Float
from orm_interface.base import Base

class CourseList(Base):
    __tablename__ = "courselist"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    provider = Column(String)
    level = Column(String)
    instructor = Column(String)
    description = Column(String)
    duration = Column(Float)
    price = Column(Float)
    link = Column(String)
    category = Column(String)

    def __init__(self, id, name, provider, level, instructor, description, duration, price, link, category):
        self.id = id
        self.name = name
        self.provider = provider
        self.level = level
        self.instructor = instructor
        self.description = description
        self.duration = duration
        self.price = price
        self.link = link
        self.category = category
