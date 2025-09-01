from pydantic import BaseModel, ConfigDict

from app.schemas.company import CompanyOut
from app.schemas.task import TaskOut


class UserBase(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str
    company_id: int


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company: CompanyOut
    tasks: list[TaskOut]
