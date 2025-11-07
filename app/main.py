from fastapi import FastAPI , Depends
from app.db.session import init_db
from contextlib import asynccontextmanager
from app.routes import auth

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Startup code
    init_db()
    yield  # everything after this is shutdown code
    # Shutdown code (optional cleanup)

app = FastAPI(title="Email Microservice")

app.include_router(auth.router)

from app.depends.auth_dep import get_current_user

@app.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"email": current_user.email, "message": "You are authorized!"}

@app.get("/")
def root():
    return {"message": "Email Service API is running "}
