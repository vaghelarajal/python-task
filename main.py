from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes.auth import router as auth_router


app = FastAPI(title="SignUp API")


# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create DB tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is working!"}


# Register routes
app.include_router(auth_router)
