from fastapi import APIRouter, Depends, HTTPException, Response ,Request
from sqlalchemy.orm import Session
from models.database import get_db
from models.user import User
from schemas.user_Schema import UserLoginSchema
from utils.jwt_generator import create_access_token
from utils.uuid_generator import generate_uuid
from utils.response import get_response
from passlib.context import CryptContext # type: ignore

router = APIRouter()

# hash handle
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login_user(user: UserLoginSchema, response: Response , db: Session = Depends(get_db) ):
    user_in_db = db.query(User).filter(User.email == user.email).first()
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    if not pwd_context.verify(user.password, user_in_db.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    access_token = create_access_token(data={"user_id": user_in_db.id})

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=30 * 60, 
        httponly=True,  
        secure=True,  
        samesite="Lax",
    )

    return get_response(
        message="You are logged in successfully",
        meta={
            "jwt_token" : access_token
        }
    )




@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return get_response(message="You have been logged out successfully")