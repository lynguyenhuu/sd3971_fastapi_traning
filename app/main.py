from fastapi import FastAPI, APIRouter

from app.api import router_user, router_task, router_company, router_auth

app = FastAPI()

api_router = APIRouter()
api_router.include_router(router_auth.router)
api_router.include_router(router_company.router)
api_router.include_router(router_user.router)
api_router.include_router(router_task.router)

app.include_router(api_router)
