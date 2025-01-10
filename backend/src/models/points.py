from sqlalchemy import Column, ForeignKey, Integer, DateTime , String
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Points(Base):
    __tablename__ = "user_points"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, default=5)  # مقدار اولیه 5 امتیاز
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
