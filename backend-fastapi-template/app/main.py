from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.roles.router import router as roles_router
from app.files.router import router as files_router
from app.tasks.router import router as tasks_router
from app.email.router import router as email_router
from app.notifications.router import router as notifications_router
from app.ai.ai_summarizer.router import router as ai_summarizer_router
from app.ai.ai_sentiment.router import router as ai_sentiment_router
from app.ai.ai_tts.router import router as ai_tts_router
from app.ai.ai_stt.router import router as ai_stt_router

from app.core.database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(files_router)
app.include_router(tasks_router)
app.include_router(email_router)
app.include_router(notifications_router)
app.include_router(ai_summarizer_router)
app.include_router(ai_sentiment_router)
app.include_router(ai_tts_router)
app.include_router(ai_stt_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
