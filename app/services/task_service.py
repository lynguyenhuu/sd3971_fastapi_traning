from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_tasks_for_user(self, user_id: int, admin=False):
        if admin:
            return self.db.query(Task).limit(10).all()
        return (
            self.db.query(Task).filter(Task.user_id == user_id).limit(10).all()
        )

    def create_task(self, user_id: int, task_in: TaskCreate) -> Task:
        task = Task(
            user_id=user_id,
            summary=task_in.summary,
            description=task_in.description,
            status=task_in.status,
            priority=task_in.priority,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(
        self, current_user, task_id: int, task_update: TaskUpdate
    ) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # check permissions
        if task.user_id != current_user.user_id and not current_user.is_admin:
            raise HTTPException(
                status_code=403, detail="Not enough permissions"
            )

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, user_id: int, task_id: int, is_admin: bool):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # check permissions
        if task.user_id != user_id and not is_admin:
            raise HTTPException(
                status_code=403, detail="Not enough permissions"
            )

        self.db.delete(task)
        self.db.commit()
        return None
