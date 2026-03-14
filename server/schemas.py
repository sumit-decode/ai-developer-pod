from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    name: str
    role: str

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
    updated_at: str

class PostHistorySchema(BaseModel):
    id: int
    post_id: int
    user_id: int
    action: str
    created_at: str