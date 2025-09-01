from pydantic import BaseModel, ConfigDict


class CompanyBase(BaseModel):
    name: str
    description: str | None = None


class CompanyOut(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
