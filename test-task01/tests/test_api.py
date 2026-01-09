import httpx

async def test_generate_slug(ac: httpx.AsyncClient):
    res = await ac.post('/short', json={"long_url": "https://my-site.ru"})
    assert res.status_code == 200