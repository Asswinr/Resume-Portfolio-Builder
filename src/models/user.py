# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String,  ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data = Column(JSON)
    pdf_path = Column(String)
    
    user = relationship("User", back_populates="resumes")

User.resumes = relationship("Resume", back_populates="user")
