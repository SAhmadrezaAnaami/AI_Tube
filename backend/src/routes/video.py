from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from models.database import get_db
from models.video import Video
from models.downloaded_video import DownloadedVideo
from downloadVideo import dwl_vid
from utils.uuid_generator import generate_uuid
from schemas.video_Schema import videoDownloadSchema
from utils.response import get_response
from utils.jwt_generator import decode_access_token
import os

router = APIRouter()

@router.post("/video/download")
def download_video(video_id: videoDownloadSchema,request : Request, db: Session = Depends(get_db)):
    try:
        auth_header = request.headers.get("access_token")

        if not auth_header:
            raise HTTPException(status_code=403, detail="Access token not provided")

        decoded_token = decode_access_token(auth_header)

        if not decoded_token:
            raise HTTPException(status_code=403, detail="Invalid access token")

        video_id = video_id.video_id
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        video_download_id  = db.query(DownloadedVideo).filter(DownloadedVideo.video_id == video_id).first()
        if not video_download_id:

            res = dwl_vid(video.video_url , video_id)

            if res == False:
                raise HTTPException(status_code=500, detail="Error downloading video")

            DV = DownloadedVideo(
                id = generate_uuid(),
                video_id = video_id,
                file_path = f"files/videos/{video_id}.3gpp",
            )

            db.add(DV)
            db.commit()

        video_Download = db.query(DownloadedVideo).filter(DownloadedVideo.video_id == video_download_id.video_id).first()
        if not video_Download:
            raise HTTPException(status_code=404, detail="Video not found")

        if not os.path.exists(video_Download.file_path):
            raise HTTPException(status_code=404, detail="Video file not found on the server")

        return FileResponse(video_Download.file_path, media_type="video/mp4", filename=f"{video_Download.video_id}.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")

from fastapi.responses import FileResponse

@router.get("/video/{video_download_id}")
def get_video_file(video_download_id: str, request : Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("access_token")

    if not auth_header:
        raise HTTPException(status_code=403, detail="Access token not provided")

    decoded_token = decode_access_token(auth_header)

    if not decoded_token:
        raise HTTPException(status_code=403, detail="Invalid access token")

    video_Download = db.query(DownloadedVideo).filter(DownloadedVideo.id == video_download_id).first()
    if not video_Download:
        raise HTTPException(status_code=404, detail="Video not found")

    if not os.path.exists(video_Download.file_path):
        raise HTTPException(status_code=404, detail="Video file not found on the server")

    return FileResponse(video_Download.file_path, media_type="video/mp4", filename=f"{video_Download.video_id}.mp4")
