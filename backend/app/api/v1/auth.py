from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from app.services.auth_service import auth_service
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, user_in)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.put("/me", response_model=UserResponse)
def update_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update profile information such as name, email and currency standard."""
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name.strip()
    if user_in.email is not None and user_in.email != current_user.email:
        existing = db.query(User).filter(User.email == user_in.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )
        current_user.email = user_in.email
    if user_in.preferred_currency is not None:
        current_user.preferred_currency = user_in.preferred_currency
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)

