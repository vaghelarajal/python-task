from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Auth API", version="1.0.0")

frontend_urls = os.getenv("FRONTEND_URLS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_urls,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}
