from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
import logging

import models
import utily
from database import get_db, engine
import schemas
import crud

models.Base.metadata.create_all(engine)
app = FastAPI(debug=True)

templates = Jinja2Templates(directory='template')

logging.basicConfig(level=logging.INFO)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/translate/', response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print(request.text, request.languages)
    task = crud.create_translation_task(db, request.text, request.languages)
    background_tasks.add_task(utily.perform_translation, task.id, request.text, request.languages, db)
    return {"task_id": task.id}


@app.get('/translate/{task_id}/', response_model=schemas.TranslationStatus)
def translate_status(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {"task_id": task.id, "status": task.status}


@app.get('/translate/content/{task_id}/', response_model=schemas.TranslationContent)
def translate_status(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {"translations": task.translations}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
