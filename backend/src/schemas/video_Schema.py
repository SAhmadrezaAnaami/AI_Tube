from pydantic import BaseModel

class videoDownloadSchema(BaseModel):
    video_id: str
