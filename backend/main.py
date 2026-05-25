from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base, SessionLocal
from backend.models import User, Conversation, Diary, UserSettings, Agent
from backend.routers import auth, conversation, diary, dashboard, settings, user, agents
from backend.seeder import seed_agents

Base.metadata.create_all(bind=engine)

# Seed preset agents
db = SessionLocal()
try:
    seed_agents(db)
finally:
    db.close()

app = FastAPI(title="Emotion Diary API", version="0.4.0")

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
app.include_router(settings.router)
app.include_router(user.router)
app.include_router(agents.router)


@app.get("/")
async def root():
    return {"message": "Emotion Diary API is running"}
