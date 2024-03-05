from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
from crud import CRUD
from sqlalchemy.ext.asyncio import async_sessionmaker
from db import engine
from serializers import NoteModel,NoteCreateModel
from typing import List
import uuid
from models import Note
from http import HTTPStatus
# app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool
#     ratings: Optional[int] = None


# my_list = [
#     {"id": 1, "title": "title of post 1", "content": "content of post 1"},
#     {"id": 2, "title": "title of post 2", "content": "content of post 2"},
# ]


# @app.get("/posts")
# async def get_all():
#     return {"data": my_list}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_post(post: Post):
#     post_dict = post.dict()
#     post_dict["id"] = randrange(0, 100000)
#     my_list.append(post_dict)
#     return {"data": post_dict}


# @app.get("/posts/latest")
# async def get_latest_post():
#     post = my_list[-1]
#     return {"post_details": post}


# @app.get("/posts/{id}")
# async def get_post_by_id(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found"
#         )
#     return {"post_detail": post}


# @app.delete("posts/{id}")
# async def delete_post(id: int):
#     indx = find_index_post(id)
#     if indx is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID {id} does not exist",
#         )
#     my_list.pop(indx)
#     return {"message": f"Post with ID {id} successfully deleted"}


# @app.put("/posts/{id}")
# async def update_post(id: int, post: Post):
#     indx = find_index_post(id)
#     if indx is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID {id} does not exist",
#         )
#     post_dict = post.dict()
#     post_dict["id"] = id
#     my_list[indx] = post_dict
#     return {"message": f"Post with ID {id} successfully updated"}


# def find_post(id):
#     for p in my_list:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_list):
#         if p["id"] == id:
#             return i


app = FastAPI()
db = CRUD()
session = async_sessionmaker(
    bind = engine,
    expire_on_commit=False
)

@app.get("/notes", response_model=List[NoteModel])
async def get_all_notes():
    notes= await db.get_all(session)

    return notes

@app.post("/notes",status_code= HTTPStatus.CREATED )
async def create_notes(note_data:NoteCreateModel):
    new_note= Note(
        id = str (uuid.uuid4()),
        title = note_data.title,
        content = note_data.content
    )

    note = await db.add(session,new_note)
    return note


@app.get("/note/{note_id}")
async def get_note_by_id(note_id):
    note = await db.get_by_id(session ,note_id)
    return note

@app.delete("/note/{note_id}")
async def delete_note(note_id):
    note = await db.get_by_id(session, note_id)
    result = await db.delete(session, note)

    return result
@app.patch("/note/{note_id}", status_code=HTTPStatus.NO_CONTENT)
async def update_note(note_id:str, data:NoteCreateModel):
    note = await db.update(session, note_id, data={
        'title':data.title,
        'content':data.content
    })

    return note
    