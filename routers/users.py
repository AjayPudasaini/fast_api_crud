from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.database import get_db
from models.user import User
from schemas.user import UserCreate
from routers.auth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/users",  response_model=List[UserCreate], summary="Users Lists", status_code=status.HTTP_200_OK)
def get_users(db:Session = Depends(get_db), user = Depends(get_current_user)):
    if not user:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    datas = db.query(User).all()
    response_data = [{"id": data.id, "title":data.username, "content": data.email, "password": data.password} for data in datas]

    return JSONResponse({"data":response_data, "message":"Success to fetch", "status": status.HTTP_200_OK})
