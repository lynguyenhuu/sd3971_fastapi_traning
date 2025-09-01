from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    summary: str
    description: str | None = None
    status: str = 'open'
    priority: int = 1


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
