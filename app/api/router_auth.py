from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.token import Token, TokenData
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
def register_user(
    user_in: UserCreate,
    user_service: UserService = Depends(UserService),
):
    user = user_service.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    new_user = user_service.create(obj_in=user_in)
    return new_user


@router.post("/login", response_model=Token)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(UserService),
):
    """
    Authenticate user and return JWT token.
    """
    user: User = user_service.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "company_id": user.company_id,
            "is_admin": user.is_admin,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=TokenData)
def read_users_me(
    current_user: TokenData = Depends(security.get_current_user),
):
    """
    Get current logged-in user profile.
    """
    return current_user
