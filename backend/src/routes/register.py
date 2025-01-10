from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.uuid_generator import generate_uuid
from models.database import get_db
from models.user import User
from models.points import Points
from schemas.user_Schema import UserCreateSchema
from utils.response import get_response
from passlib.context import CryptContext # type: ignore

router = APIRouter()

# manage hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/register")
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user_Email = db.query(User).filter(User.email == user.email).first()
    existing_user_Username= db.query(User).filter(User.username == user.username).first()
    if existing_user_Email:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    if existing_user_Username:
        raise HTTPException(status_code=400, detail="User with this username already exists.")

    new_user = User(
        id=generate_uuid(),
        username=user.username,
        email=user.email,
        password_hash=pwd_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()

    points = Points(id=generate_uuid(),
                    user_id=new_user.id,
                    points=999)
    db.add(points)
    db.commit()

    return get_response(
        message= "User registered successfully.",
        meta= {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        },
        code=201
    )
