from fastapi import Depends, Request, APIRouter, HTTPException, status
from app.service import ApiReq
from app.exceptions import GetInfoError, GetTokenError

api_router = APIRouter(prefix='/api_reqs', tags=["API_router"])

def get_service(request: Request) -> ApiReq:
    email = ''
    token = 'asd09123ka;dlk-0=-asd='
    password = ''

    return ApiReq(email=email, token=token, password=password, session=request.app.state.client_session)

@api_router.get('/get-info')
async def get_info(service: ApiReq = Depends(get_service)):
    try:
        return await service.get_info()
    except GetInfoError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    
@api_router.get('/auth')
async def auth(service: ApiReq = Depends(get_service)):
    try:
        return await service.auth()
    except GetTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )