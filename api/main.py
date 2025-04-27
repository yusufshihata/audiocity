from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="Audiocity Audio Editing API",
    description="API for audio editing and processing using the Audiocity engine",
    version="0.1.0"
)
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
