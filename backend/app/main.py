from fastapi import FastAPI

app = FastAPI(
    title="Atlas",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    return {"status": "ok",
    "service":"Atlas"}


@app.get("/")
async def home():
    return {
        "message": "Atlas API is running ",
        "documentation": "/docs",
        "health_check": "/health" 
    }
