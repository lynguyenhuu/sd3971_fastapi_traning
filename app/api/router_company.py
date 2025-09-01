from fastapi import APIRouter, Depends

from app.schemas.company import CompanyOut
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[CompanyOut])
def list_companies(
    company_service: CompanyService = Depends(CompanyService),
):
    companies = company_service.get_companies()
    return companies
