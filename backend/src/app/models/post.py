from sqlalchemy import Column, String, DateTime
import datetime

from app.db.base_class import Base


class Post(Base):
    image_url = Column(String)
    title = Column(String)
    content = Column(String)
    creator = Column(String)
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.now())
