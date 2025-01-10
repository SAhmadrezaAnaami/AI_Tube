from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , Session

DATABASE_URL = "sqlite:///./DB/app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from models.user import User
    from models.points import Points
    from models.search import Search
    from models.video import Video
    from models.downloaded_video import DownloadedVideo
    Base.metadata.create_all(bind=engine)
    
def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
