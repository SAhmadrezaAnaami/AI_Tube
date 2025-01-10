from sqlalchemy import Column, Integer, String, DateTime , ForeignKey
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class JWToken(Base):
    __tablename__ = "jwt_tokens"

    id = Column(String, primary_key=True, nullable= False)
    user_id = Column(String, ForeignKey("users.id"),nullable= False)
    token = Column(String, unique=True, nullable= False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User")

    def __init__(self,id:str , token: str,user_id:str , ttl_minutes: int = 1):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
