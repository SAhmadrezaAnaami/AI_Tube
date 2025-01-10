from fastapi import APIRouter, HTTPException, Depends , Request
from sqlalchemy.orm import Session
from models.database import get_db
from models.search import Search
from models.video import Video
from models.points import Points
from schemas.search_Schema import searchSchema
import concurrent.futures
from utils.encodeImage import encode_image
from utils.youTubeSearch import search_youtube , test
from utils.uuid_generator import generate_uuid
from utils.downloadThumbnail import download_thumbnail
from utils.response import get_response
from utils.jwt_generator import decode_access_token

from LLM.gemini import Genai
from prompts.getVideo import getVideoPrompts

from dotenv import load_dotenv
import os

load_dotenv()

t = os.getenv('GEMINI_KEY')
model = Genai(t , sys_instruct=getVideoPrompts)

router = APIRouter()

@router.post("/search")
def search_videos(search: searchSchema, request:Request ,db: Session = Depends(get_db)):

    auth_header = request.headers.get("access_token")

    if not auth_header:
        raise HTTPException(status_code=403, detail="Access token not provided")

    decoded_token = decode_access_token(auth_header)

    if not decoded_token:
        raise HTTPException(status_code=403, detail="Invalid access token")

    points = db.query(Points).filter(Points.user_id == decoded_token['user_id']).first()

    if not points:
        raise HTTPException(status_code=403, detail="User not found")

    if points.points == 0:
        raise HTTPException(status_code=403, detail="Insufficient points")

    # check if search.searchText does not exist before add to Search
    existing_search = db.query(Search).filter(Search.search_text == search.searchText).first()
    if existing_search:
        videos = db.query(Video).filter(Video.search_id == existing_search.id).all()
        res = []
        for video in videos:
            video.thumbnail = encode_image(video.thumbnail_path)

        return get_response(
            message="Search already exists",
            data = videos,
            meta={
                "search_id": existing_search.id
            }
        )

    searchRecord = Search(id= generate_uuid(),
                    search_text= search.searchText,
                    user_id = decoded_token['user_id'])
    db.add(searchRecord)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(model.generate_text, search.searchText)
        try:
            modelRes = future.result(timeout=3)  # Wait for up to `timeout` seconds
        except concurrent.futures.TimeoutError:
            raise HTTPException(status_code=500, detail="Keyword generation took too long")

    if modelRes['status'] == "error" :
        raise HTTPException(status_code=500, detail="Error in generating keywords")

    res = []
    for keyword in modelRes['data'].split("-"):

        videoSearchResult = search_youtube(keyword)
        for vsr in videoSearchResult:
            try:
                existing_video = db.query(Video).filter(Video.id == vsr["id"]).first()
                if not existing_video:
                    print("data Not exists")

                    download_thumbnail(vsr['thumbnails'][0], vsr["id"])

                    new_video = Video(
                        id=vsr["id"],
                        search_id=searchRecord.id,
                        title=vsr["title"],
                        description=vsr["long_desc"],
                        duration=vsr["duration"],
                        thumbnail_path=f"files/thumbnails/{vsr['id']}.jpg",
                        video_url="https://www.youtube.com" + vsr["url_suffix"],
                        creator= vsr['channel']
                    )
                    db.add(new_video)
                    db.commit()

                res.append({
                    "id": vsr["id"],
                    "title": vsr["title"],
                    "description": vsr["long_desc"],
                    "duration": vsr["duration"],
                    "thumbnail":encode_image(f"files/thumbnails/{vsr['id']}.jpg"),
                    "video_url": "https://www.youtube.com" + vsr["url_suffix"],
                    "creator": vsr['channel']
                })

            except Exception as e:
                pass

    points.points = points.points - 1
    db.commit()

    return get_response(
        message= "video retrieved successfully",
        data= res,
        meta= {
            "search_id" : searchRecord.id,
        }
    )


@router.get("/search/{search_id}")
def get_search_results(search_id: str,request:Request, db: Session = Depends(get_db)):

    auth_header = request.headers.get("access_token")

    if not auth_header:
        raise HTTPException(status_code=403, detail="Access token not provided")

    decoded_token = decode_access_token(auth_header)

    if not decoded_token:
        raise HTTPException(status_code=403, detail="Invalid access token")

    search = db.query(Search).filter(Search.id == search_id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")

    videos = db.query(Video).filter(Video.search_id == search_id).all()

    #change videos thumbnail_path to thumbnail_file base64
    for video in videos:
        video.thumbnail = encode_image(video.thumbnail_path)

    if not videos:
        raise HTTPException(status_code=404, detail="No videos found for this search")

    return get_response(
        message = "video retrieved successfully",
        data= videos,
        meta={
            "search_id": search_id
        }
    )
