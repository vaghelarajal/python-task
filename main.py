from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router

# Simple, fast startup
app = FastAPI(title="Auth API", version="1.0.0")

# Minimal CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# add authentication routes
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}
