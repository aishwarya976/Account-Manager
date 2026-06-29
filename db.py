from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

password = quote_plus("m@t@l@kshmi")

DATABASE_URL=f"postgresql://username:password@localhost:port/account_manager"

engine=create_engine(DATABASE_URL)


SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base=declarative_base()

Base.metadata.create_all(bind=engine)

db=SessionLocal()

def get_db():

 try:
    yield db
 finally:
  db.close()    




