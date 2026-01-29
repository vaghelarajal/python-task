from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from sqlalchemy import Column, Integer, String


app = FastAPI(title="FastAPI + React + Postgres Test")


# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test table mapping
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is working!"}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/users")
def create_user(db: Session = Depends(get_db)):
    user = User(username="Rajal", email="rajal@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
