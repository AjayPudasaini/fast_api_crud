from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.database import get_db
from models.posts import Post
from schemas.post import CreatePost

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[CreatePost], status_code=status.HTTP_200_OK)
def get_all_posts(db:Session = Depends(get_db)):
    datas = db.query(Post).all()
    response_data = [{"id": data.id, "title":data.title, "content": data.content} for data in datas]

    return JSONResponse({"data":response_data, "message":"Success to fetch", "status": status.HTTP_200_OK})



@router.get("/{id}", response_model=CreatePost, status_code=status.HTTP_200_OK)
def get_single_posts(id:int, db:Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not Found")
    
    response_data = {
        "title": post.title,
        "content": post.content,
    }

    return JSONResponse({"data":response_data, "message":"Success to fetch", "status": status.HTTP_200_OK})


@router.post('/create', response_model=CreatePost, status_code=status.HTTP_201_CREATED)
def create_post(post:CreatePost,  db:Session=Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    response_data = {
        "title": new_post.title,
        "content": new_post.content,
    }

    return JSONResponse({"data":response_data, "message":"posts created", "status": status.HTTP_201_CREATED})


@router.patch("/{id}/update", response_model=CreatePost, status_code=status.HTTP_200_OK)
def update_post(post:CreatePost, id:int, db: Session=Depends(get_db)):
    instance = db.query(Post).filter(Post.id == id).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Post Not Found")
    
    # Update instance attributes
    instance.title = post.title
    instance.content = post.content

    db.commit()

    response_data = {
        "title":instance.title,
        "content":instance.content,
    }
    return JSONResponse({"data":response_data, "message":"posts updated", "status": status.HTTP_200_OK})


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    instance = db.query(Post).filter(Post.id==id).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Post Not Found")
    
    db.delete(instance)
    db.commit()


    return JSONResponse({"data":[], "message":"Post deleted success", "status":status.HTTP_204_NO_CONTENT})


