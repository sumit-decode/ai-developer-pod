from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, role={self.role})'

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', backref='posts')
    created_at = Column(String)
    updated_at = Column(String)

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, author_id={self.author_id}, created_at={self.created_at}, updated_at={self.updated_at})'

class PostHistory(Base):
    __tablename__ = 'post_history'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String)
    created_at = Column(String)

    def __repr__(self):
        return f'PostHistory(id={self.id}, post_id={self.post_id}, user_id={self.user_id}, action={self.action}, created_at={self.created_at})'