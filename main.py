from fastapi import FastAPI, HTTPException, status

app = FastAPI()

db = [
    {"id": 0, "title": "Task 1", "done": True}, 
    {"id": 1, "title": "Task 2", "done": False}, 
    {"id": 2, "title": "Task 3", "done": False}, 
    {"id": 3, "title": "Task 4", "done": False} 
    ]

# @app.get('/')
# async def root():
#     return{"message": "Hello World!"}

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
    if(int(id)>len(db)):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Item with id: {id} was not found."
        ) 
    else:
        return db[int(id)]



