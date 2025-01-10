from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    search_id = Column(String, ForeignKey("searches.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    duration = Column(String)
    thumbnail_path = Column(String)
    video_url = Column(String)
    creator = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    search = relationship("Search")
