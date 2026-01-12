from sqlalchemy.ext.asyncio import AsyncSession
from app.models.products import Product
from app.schemas.products import ProductCreate
from app.schemas.exceptions.products import ProductCreateError, ProductExistsException, ProductReadError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class ProductService():
    @staticmethod
    async def product_create(data: ProductCreate, session: AsyncSession) -> Product:
        result = await session.execute(select(Product).where(Product.title == data.title))
        exists = result.scalar_one_or_none()

        if exists:
            raise ProductExistsException('Продукт существует')

        product = Product(**data.model_dump())
        session.add(product)

        try:
            await session.commit()
            await session.refresh(product)
        except SQLAlchemyError as e:
            await session.rollback()
            raise ProductCreateError(f"Ошибка создания продукта: {str(e)}")
        
        return product
    

    @staticmethod
    async def get_all_products(session: AsyncSession) -> list[Product]:
        try:
            res = await session.execute(select(Product))
            data = res.scalars().all() or []
            return data
        except SQLAlchemyError as e:
            raise ProductReadError(f"Ошибка получения продуктов: {str(e)}")


