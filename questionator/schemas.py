from typing import List, Optional

from pydantic import BaseModel, UUID4

class HTTPError(BaseModel):
    detail: str

class AnswerBase(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

class AnswerCreate(AnswerBase):
    title: str
    author: str

class AnswerInDBBase(AnswerBase):
    id: Optional[UUID4] = None
    question_id: UUID4

    class Config:
        orm_mode = True

class Answer(AnswerInDBBase):
    pass

class QuestionBase(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

class QuestionCreate(QuestionBase):
    title: str
    author: str

class QuestionInDBBase(QuestionBase):
    id: Optional[UUID4] = None
    answers: List[Answer] = []

    class Config:
        orm_mode = True

class Question(QuestionInDBBase):
    pass
