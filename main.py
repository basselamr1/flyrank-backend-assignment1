from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title:str
    done: bool = False
    
db = [
    {"id": 0, "title": "Task 1", "done": True}, 
    {"id": 1, "title": "Task 2", "done": False}, 
    {"id": 2, "title": "Task 3", "done": False}, 
    {"id": 3, "title": "Task 4", "done": False}
    ]

@app.get("/")
async def get_api_description():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def get_server_status():
    return {"status": "ok"}

@app.get('/tasks')
async def get_tasks():
    return db

@app.get('/tasks/{id}')
async def get_task(id):
    task = next((item for item in db if item["id"] == id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id: {id} was not found."
        ) 
    return task

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
async def add_task(task: Task):
    new_id = max((item['id'] for item in db), default = 0) + 1

    if(not task.title or task.title==""):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title can't be empty."
        )

    new_task = {
        "id": new_id,
        "title": task.title, 
        "done": task.done
    }

    db.append(new_task)
    return new_task, db

@app.put('/tasks/{id}')
async def update_task(task:Task, id):
    if int(id) > len(db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id: {id} not found."
        )
    if task.title =="" and task.done == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Empty body: You must provide a title or done status."
        )
    existing_task = db[int(id)-1]
    if task.title is not None:
        existing_task['title'] = task.title
    
    if task.done is not None:
        existing_task['done'] = task.done
    
    return existing_task, db

@app.delete('/tasks/{id}',status_code= status.HTTP_204_NO_CONTENT)
async def delete_task(id):
    if int(id) > len(db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Unknown task id."
        )
    del db[int(id)-1]
    return db
    
