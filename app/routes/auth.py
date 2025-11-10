from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.db.models import User
from app.schemas.auth import UserCreate, UserRead, Token
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


# Signup
@router.post("/signup", response_model=UserRead)
def signup(user: UserCreate, db: Session = Depends(get_session)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print("DEBUG password type:", type(user.password))
    print("DEBUG password value:", user.password)
    new_user = User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Login
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_session)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
