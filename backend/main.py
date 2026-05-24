from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
from backend.models import User, Conversation, Diary  # noqa: ensure models loaded
from backend.routers import auth, conversation, diary, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Emotion Diary API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(conversation.router)
app.include_router(diary.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    return {"message": "Emotion Diary API is running"}
