from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.clip_api import router as api_router
from backend.config import OUTPUT_DIR, API_HOST, API_PORT
import uvicorn
import os

app = FastAPI(title="NEXUS VIDEO AGENT API")

# Mount outputs directory to serve clipped videos
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to NEXUS VIDEO AGENT API"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=API_HOST, port=API_PORT, reload=True)
