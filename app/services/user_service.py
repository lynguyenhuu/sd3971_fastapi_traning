from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.hashing import Hasher

from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.get_by_username(username)
        if not user:
            return None
        if not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    def get_users_by_company_id(self, company_id: int):
        return (
            self.db.query(User)
            .filter(User.company_id == company_id)
            .limit(10)
            .all()
        )

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, obj_in: UserCreate) -> User:
        db_user = User(
            username=obj_in.username,
            name=obj_in.first_name + " " + obj_in.last_name,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            hashed_password=Hasher.get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_admin=obj_in.is_admin,
            company_id=obj_in.company_id,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
