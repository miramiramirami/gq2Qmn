from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.product_rep import ProductRepository
from app.tests.conftest import test_session
from app.schemas.product import ProductCreate

def test_root(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
    assert response.json() == {
        'message': 'Welcome to fastapi shop API',
        "docs": "api/docs",
    }

def test_get_products(test_client):
    response = test_client.get('/api/products')

    assert  response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "products" in data
    print(data)


def test_product_rep_get_all(test_session):
    repository = ProductRepository(db=test_session)

    response = repository.get_all()
    assert type(response) == list
    print(response)


def test_product_rep_create(test_session):
    repository = ProductRepository(db=test_session)

    payload = ProductCreate(
        name= "12345623",
        description= None,
        price= 12.5,
        category_id= 1,
        image_url= None,
    )

    response = repository.create(payload)
    print(response)






