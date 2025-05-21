from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config.db import get_database
from app.routers.user import router as user_router
from app.routers.chat import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.on_event("startup")
async def startup_event():
    try:
        db = await anext(get_database())
        result = await db.command("ping")
        print("🚀 MongoDB connected:", result)
    except Exception as e:
        print("❌ Failed to connect to MongoDB:", str(e))

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 FastAPI app is shutting down.")

@app.get("/")
async def root():
    return {"message": "Welcome to the MongoDB-powered FastAPI app!"}

@app.get("/ping-db")
async def ping_db(db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        result = await db.command("ping")
        return {"status": "success", "details": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
