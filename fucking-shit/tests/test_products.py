import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.products import ProductCreate
from app.services.products import ProductService
from app.schemas.exceptions.products import ProductExistsException
from app.models.products import Product
from typing import AsyncGenerator
from sqlalchemy import text

@pytest.mark.asyncio
async def test_create_product(ac: AsyncClient):
    payload = {
        'title': "Prod a",
        "description": "First test",
        "price": 100.5
    }

    res = await ac.post('/products/', json=payload)

    assert res.status_code == 200, f"Response: {res.text}"

    data = res.json()
    
    assert 'id' in data
    assert data['title'] == payload['title']
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]

    print(data)


@pytest.mark.asyncio
async def test_get_products(ac: AsyncClient):
    res = await ac.get('/products/')

    assert res.status_code == 200 

    data = res.json()

    print(data)

    for product in data:
        assert "id" in product
        assert "title" in product
        assert "description" in product
        assert "price" in product
        

@pytest.mark.asyncio
async def test_create_product_service(session: AsyncSession):
    payload = ProductCreate(title="test product", description="A test", price=123.45)
    product = await ProductService.product_create(payload, session)
    
    assert isinstance(product, Product)
    assert product.id is not None
    assert product.title == payload.title
    assert product.description == payload.description
    assert product.price == payload.price


@pytest.mark.asyncio
async def test_create_duplicate_product_raises(session: AsyncSession):
    payload = ProductCreate(title="Duplicate Product", description="First", price=50)
    await ProductService.product_create(payload, session)


    with pytest.raises(ProductExistsException):
        await ProductService.product_create(payload, session)



@pytest_asyncio.fixture
async def clean_session(session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    await session.execute(text("DELETE FROM products"))
    await session.commit()
    yield session


@pytest.mark.asyncio
async def test_get_all_products_service(clean_session: AsyncSession):
    session = clean_session
    products = [
        ProductCreate(title=f"Prod {i}", description=f"Desc {i}", price=i*10)
        for i in range(3)
    ]

    for p in products:
        await ProductService.product_create(p, session)

    all_products = await ProductService.get_all_products(session)

    assert len(all_products) == 3
    titles = [p.title for p in all_products]
    for p in products:
        assert p.title in titles