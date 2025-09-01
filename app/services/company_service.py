from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.company import Company


class CompanyService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_companies(self):
        return self.db.query(Company).limit(10).all()
