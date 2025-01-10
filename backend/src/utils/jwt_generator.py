from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta

# JWT configuration
SECRET_KEY = "AI_TUBE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 14400

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # Handle decoding errors
        return False
