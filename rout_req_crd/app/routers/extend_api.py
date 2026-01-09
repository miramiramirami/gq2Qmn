from fastapi import APIRouter, Depends, Request
from app.services.extend_api import TestApi

router = APIRouter(prefix='/extend_api', tags=["api"])


def get_service(request: Request):
    token = 'asdsa-asdasdSADsad21312asd'
    user = 'user'
    password = 'passwd'
    return TestApi(token=token, user=user, password=password, session=request.app.state.session) 


@router.get('/')
async def return_hi(service: TestApi = Depends(get_service)):
    return await service.get_bin()

@router.get('/auth')
async def auth(service: TestApi = Depends(get_service)):
    return await service.auth()

@router.get('/bearer-auth')
async def auth(service: TestApi = Depends(get_service)):
    return await service.bearer_auth()