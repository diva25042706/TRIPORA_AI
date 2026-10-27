from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def register_user(self, db: Session, user_in: UserCreate) -> User:
        existing = db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )
        
        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            full_name=user_in.full_name or user_in.email.split("@")[0].title(),
            preferred_currency=user_in.preferred_currency or "INR"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

auth_service = AuthService()
