from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class DownloadedVideo(Base):
    __tablename__ = "downloaded_videos"

    id = Column(String, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video")
