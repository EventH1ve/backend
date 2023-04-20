import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["home"])
def greet():
    return {"success": True}
