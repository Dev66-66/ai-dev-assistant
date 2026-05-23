from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def mock_generate():
    with patch("app.services.gemini.generate", new_callable=AsyncMock) as m:
        yield m


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_ui_serves_html():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_completion(mock_generate):
    mock_generate.return_value = "    return x + y"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/completion/",
            json={"code": "def add(x, y):", "language": "python"},
        )
    assert response.status_code == 200
    assert "suggestion" in response.json()


@pytest.mark.asyncio
async def test_completion_default_language(mock_generate):
    mock_generate.return_value = "    pass"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/completion/", json={"code": "def foo():"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_tests_gen(mock_generate):
    mock_generate.return_value = "def test_add():\n    assert add(1, 2) == 3"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/tests/",
            json={"code": "def add(x, y):\n    return x + y"},
        )
    assert response.status_code == 200
    assert "tests" in response.json()


@pytest.mark.asyncio
async def test_docs_gen(mock_generate):
    mock_generate.return_value = "Add two numbers together."
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/docs/",
            json={"code": "def add(x, y):\n    return x + y"},
        )
    assert response.status_code == 200
    assert "docstring" in response.json()


@pytest.mark.asyncio
async def test_docs_gen_with_style(mock_generate):
    mock_generate.return_value = "Multiply a by b.\n\nArgs:\n    a: first.\n    b: second."
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/docs/",
            json={"code": "def mul(a, b):\n    return a * b", "style": "numpy"},
        )
    assert response.status_code == 200
    assert response.json()["docstring"] != ""
