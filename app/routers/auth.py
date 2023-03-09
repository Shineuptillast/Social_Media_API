from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils
from ..schemas import Userlogin
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..oauth2 import *
router = APIRouter(tags=[
    'Authentication'
])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user_data = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentails")

    # Create a token
    access_token = create_access_token(data={"user_id": user_data.id})

    # return a token

    return {"access_token": access_token, "token_type": "bearer"}
