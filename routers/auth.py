from datetime import timedelta, datetime
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.database import get_db
from models.user import User
from schemas.user import UserCreate, Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SECRET_KEY = "_zoOs1WIfZpt89vemGN5guFRnZA5OnyNAqYoG1C9GHK5GPHmA0Iv2hoPNA2Yv_OdEX7kl9gp"
ALGORITHM = "HS256"

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user_register: UserCreate, db:Session=Depends(get_db)):
    new_user = User(
        username=user_register.username,
        password=bycrypt_context.hash(user_register.password),
        email=user_register.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(username:str, password:str, db):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bycrypt_context.verify(password, user.password):
        return True
    return user

def create_access_token(username:str, user_id:int, exp:timedelta):
    expires = datetime.utcnow() + exp
    encode = {"un": username, "id": user_id, "exp": expires}
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



@router.post("/login", response_model=Token)
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        user.username,
        user.id,  
        timedelta(minutes=15)
    )

    return JSONResponse({"access_token": access_token, "token_type": "bearer"})



def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("un")
        user_id = payload.get("id")
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        
        return JSONResponse({"username": username, "user_id": user_id})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.") 




