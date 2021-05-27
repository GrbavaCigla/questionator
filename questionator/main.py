from typing import Any, List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from . import actions, models, schemas
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
    questions = actions.question.get_all(db=db, skip=skip, limit=limit)
    return questions

@app.post("/questions", response_model=schemas.Question, status_code=HTTP_201_CREATED, tags=["Questions"])
def create_question(*, db: Session = Depends(get_db), post_in: schemas.QuestionCreate) -> Any:
    post = actions.question.create(db=db, obj_in=post_in)
    return post

@app.delete(
    "/questions/{id}",
    response_model=schemas.Question,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["Questions"],
)
def delete_post(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    post = actions.question.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Question not found")
    post = actions.question.remove(db=db, id=id)
    return post
