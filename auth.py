from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_content = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def hash_password(password):
    return pwd_content.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_content.verify(plain_password,hashed_password)

SECRET_KEY=".."
ALGORITHM=".."

def create_token(data):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=30)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(
        to_encode, key=..,algorithm=..
    )

    return encoded_jwt
