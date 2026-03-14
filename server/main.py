from fastapi import FastAPI
app = FastAPI()

from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str

class UserList(BaseModel):
    users: List[User]

@app.get('/users', response_model=UserList)
async def read_users():
    return []

@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    return User(id=user_id, name='John Doe')

@app.post('/users', response_model=User)
async def create_user(user: User):
    return user

@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    return {'message': f'User {user_id} deleted'}

@app.get('/posts', response_model=PostList)
async def read_posts():
    return []

# Post CRUD routes

class Post(BaseModel):
    id: int
    title: str

class PostList(BaseModel):
    posts: List[Post]

@app.get('/posts/{post_id}', response_model=Post)
async def read_post(post_id: int):
    return Post(id=post_id, title='My Post')

@app.post('/posts', response_model=Post)
async def create_post(post: Post):
    return post

@app.delete('/posts/{post_id}')
async def delete_post(post_id: int):
    return {'message': f'Post {post_id} deleted'}

# Moderation logic

@app.get('/ban/{user_id}')
async def ban_user(user_id: int):
    return {'message': f'User {user_id} banned'}