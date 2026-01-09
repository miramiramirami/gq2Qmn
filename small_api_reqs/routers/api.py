from fastapi import APIRouter, Request, Depends
from services.api import ReqResApi

router = APIRouter(prefix='/api_get_users', tags=['API'])

def get_service(requst: Request):
    email = "eve.holt@reqres.in"
    password = "cityslicka"

    return ReqResApi(email, password, session=requst.app.state.session)

@router.get('/')
async def get_list_users(api: ReqResApi = Depends(get_service)):
    return await api.get_users()