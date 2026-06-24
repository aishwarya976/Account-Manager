from db import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True)
    # password=Column(String)
    hashed_password=Column(String,unique=True)
    email=Column(String,unique=True)