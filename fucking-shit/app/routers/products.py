from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies.get_session import get_session
from app.schemas.products import ProductCreate, ProductResponse
from app.schemas.exceptions.products import ProductCreateError, ProductExistsException, ProductReadError
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.products import ProductService


router = APIRouter(prefix='/products', tags=["Products"])


@router.post('/', response_model=ProductResponse)
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await ProductService.product_create(data, session)
    except ProductExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Продукт уже существует'
        )
    except ProductCreateError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    
@router.get('/', response_model=list[ProductResponse])
async def get_all_products(session: AsyncSession = Depends(get_session)):
    try:
        return await ProductService.get_all_products(session)
    except ProductReadError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )