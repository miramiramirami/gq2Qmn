from fastapi import APIRouter, Depends, Request
from services.extend_api import ApiService

router = APIRouter(prefix="/extend_api", tags=["APIes"])


def get_user_service(request: Request) -> ApiService:
    return ApiService(request.app.state.http_client)


@router.get("/{user_id}")
async def get_result(user_id: int, service: ApiService = Depends(get_user_service)):
    return await service.get_user(user_id)
