import pytest
from httpx import AsyncClient

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