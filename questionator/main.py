from typing import Any, List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from . import models, schemas
from .db import SessionLocal, engine

# Create all tables in the database.
# Comment this out if you using migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/questions", response_model=List[schemas.Question], tags=["Questions"])
def list_questions(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    print(questions[0].answers[0].question_id)
    return questions

@app.post("/questions", response_model=schemas.Question, status_code=HTTP_201_CREATED, tags=["Questions"])
def create_question(*, db: Session = Depends(get_db), question_in: schemas.QuestionCreate) -> Any:
    obj_in_data = jsonable_encoder(question_in)
    db_obj = models.Question(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.delete(
    "/questions/{id}",
    response_model=schemas.Question,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["Questions"],
)
def delete_post(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    question = db.query(models.Question).filter(models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Question not found")

    obj = db.query(models.Question).get(id)
    db.delete(obj)
    db.commit()
    return question 

@app.post("/questions/{id}/answers/")
def create_answer(
    id: UUID4, answer_in: schemas.AnswerCreate, db: Session = Depends(get_db)
):
    db_answer = models.Answer(**answer_in.dict(), question_id=id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return answer_in