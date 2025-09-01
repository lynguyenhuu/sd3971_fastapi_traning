from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.user import UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserOut])
def list_users(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(UserService),
):
    users = user_service.get_users_by_company_id(
        company_id=current_user.company_id
    )
    return users


@router.get("/{user_id}", response_model=UserOut)
def get_user_detail(
    user_id,
    user_service: UserService = Depends(UserService),
):
    users = user_service.get_by_id(user_id=user_id)
    return users
