from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.database import get_db
from models.user import User
from models.points import Points
from models.search import Search
from utils.response import get_response
from utils.jwt_generator import decode_access_token

router = APIRouter()


@router.get("/status")
def get_status(request: Request , db: Session = Depends(get_db) ):
    
    auth_header = request.headers.get("access_token")
    if not auth_header:
        raise HTTPException(status_code=403, detail="Access token not provided")
    
    decoded_token = decode_access_token(auth_header)
    
    if not decoded_token:
        raise HTTPException(status_code=403, detail="Invalid access token")
        
    user_record = db.query(User).filter(User.id == decoded_token['user_id']).first()
    point_record = db.query(Points).filter(Points.user_id == decoded_token['user_id']).first()
    Search_record = db.query(Search).filter(Search.user_id == decoded_token['user_id']).all()
    
    return get_response(
        message= "success",
        meta={
           "user_record" : user_record,
           "point_record" : point_record,
           "Search_record" : Search_record,
        }
    )