from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import db, Base, engine, get_db
from models import User
from auth import hash_password, create_token, verify_password


Base.metadata.create_all(bind=engine)

app=FastAPI()

class Update(BaseModel):
   email:str
   username:str
   password:str
   new_password:str

class Login(BaseModel):
    email:str
    username:str
    password:str    

class TokenResponse(BaseModel):
   access_token:str

@app.post("/sign_up")
def create_account(req:Login, db: Session = Depends(get_db)):
    try :
        hashed_pw=hash_password(req.password)

        new_user=User(
            username=req.username,
            email=req.email,
            hashed_password=hashed_pw
        )
        print(str(new_user))

        # save to database

        db.add(new_user)
        print("Add Successful")

        db.commit()
        print("Commit")

        db.refresh(new_user)
        print("Updated")

        return{"message":"User created"}

    except Exception as e:
     print("ERROR:", str(e))
     raise

@app.post("/login",response_model=TokenResponse)
def login_account(req:Login, db:Session=Depends(get_db)):
    print(str(req))
    login_user=db.query(User).filter (User.username==req.username).first()

    if not login_user:
     raise HTTPException(
        status_code=404,
        detail="User not found"
     )
    
    if not verify_password(req.password,login_user.hashed_password):
     raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access Denied. Wrong Username or password"
     )
    
    else:
     token=create_token({"sub":login_user.username})
     return{"access_token":token}
    
    
@app.put("/change_password")
def change_password(req:Update, db:Session=Depends(get_db)):
   
   updatepw=db.query(User).filter(User.username==req.username).first()

   if not updatepw:
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Access Denied. Wrong Username or Password"
     )
   
   if not verify_password(req.password,updatepw.hashed_password):
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Access Denied. Wrong Username or password"
      )
   
   else:
    updatepw.hashed_password=hash_password(req.new_password)
    db.commit()
    db.refresh(updatepw)
    print("Password changed successfully")
    return{"message":"Password updated"}
   
@app.delete("/delete_account")
def delete_account(req:Login, db:Session=Depends(get_db)):
   deleteac=db.query(User).filter(User.username==req.username).first()
   
   if not deleteac:
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Access Denied. Wrong Username or Password"
     )
   
   if not verify_password(req.password,deleteac.hashed_password):
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Access Denied. Wrong Username or password"
      )
      
   else:
    deleteac.hashed_password=hash_password(req.password)
    db.commit()
    db.refresh(deleteac)
    print("Account Deleted Successfully")
    return{"message":"Account Deleted"}
   