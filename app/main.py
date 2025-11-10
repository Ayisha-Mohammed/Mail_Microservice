from fastapi import FastAPI, Depends
from app.db.session import init_db
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from app.routes import auth, email

# from app.db.session import get_session
# from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.auth import ProtectedResponse
from slowapi.middleware import SlowAPIMiddleware
from app.rate_limiter import limiter, rate_limit_exceeded_handler
from fastapi.responses import JSONResponse
from fastapi import Request
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield  # everything after this is shutdown code
    # Shutdown code (optional cleanup)


app = FastAPI(title="Email Microservice", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(email.router)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )


from app.depends.auth_dep import get_current_user


@app.get("/protected", response_model=ProtectedResponse)
def protected_route(current_user=Depends(get_current_user)):
    return {"email": current_user.email, "message": "You are authorized!"}


@app.get("/")
def root():
    return {"message": "Email Service API is running "}


# @app.get("/check-db")
# def check_db_connection(db: Session = Depends(get_session)):
#     try:
#         db.execute(text("SELECT 1"))
#         return {"status": "Database connection successful"}
#     except Exception as e:
#         return {"status": "Database connection failed", "error": str(e)}
