from fastapi import FastAPI

app = FastAPI()

# @app.get('/')
# async def root():
#     return{"message": "Hello World!"}

@app.get("/")
async def get_api_description():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def get_server_status():
    return {"status": "ok"}