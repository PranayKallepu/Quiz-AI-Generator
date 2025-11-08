from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


# SQLAlchemy Model
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    date_generated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    scraped_content = Column(Text, nullable=True)
    full_quiz_data = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"


# Pydantic Schemas
class QuestionOption(BaseModel):
    text: str
    is_correct: bool


class Question(BaseModel):
    question: str
    options: List[QuestionOption]
    explanation: Optional[str] = None


class QuizData(BaseModel):
    summary: str
    questions: List[Question]


class QuizCreate(BaseModel):
    url: HttpUrl
    title: str
    scraped_content: Optional[str] = None
    full_quiz_data: Dict[str, Any]


class QuizResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    url: str
    title: str
    date_generated: datetime
    full_quiz_data: Dict[str, Any]


class QuizListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    url: str
    title: str
    date_generated: datetime


class QuizGenerateRequest(BaseModel):
    url: str

