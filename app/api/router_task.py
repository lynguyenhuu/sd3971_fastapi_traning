from fastapi import APIRouter, Depends
from starlette import status

from app.core.security import get_current_user
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    current_user=Depends(get_current_user),
    task_service: TaskService = Depends(TaskService),
):
    tasks = task_service.get_tasks_for_user(
        user_id=current_user.user_id, admin=current_user.is_admin
    )
    return tasks


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    current_user=Depends(get_current_user),
    task_service: TaskService = Depends(TaskService),
):
    return task_service.create_task(
        user_id=current_user.user_id, task_in=task_in
    )


@router.patch("/{task_id}", response_model=TaskOut)
def patch_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user=Depends(get_current_user),
    task_service: TaskService = Depends(TaskService),
):
    return task_service.update_task(
        current_user=current_user, task_id=task_id, task_update=task_update
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id,
    current_user=Depends(get_current_user),
    task_service: TaskService = Depends(TaskService),
):
    return task_service.delete_task(
        user_id=current_user.user_id,
        task_id=task_id,
        is_admin=current_user.is_admin,
    )
