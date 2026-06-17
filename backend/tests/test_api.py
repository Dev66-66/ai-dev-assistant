from unittest.mock import AsyncMock, patch

import pytest
from app.main import app
from app.services.text import strip_fences
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def mock_generate():
    with patch("app.services.llm.generate", new_callable=AsyncMock) as m:
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


@pytest.mark.asyncio
async def test_completion_llm_error():
    with patch("app.services.llm.generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = RuntimeError("LLM unavailable")
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/completion/",
                json={"code": "def foo():"},
            )
    assert response.status_code == 503


@pytest.mark.asyncio
async def test_tests_gen_llm_error():
    with patch("app.services.llm.generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = RuntimeError("LLM unavailable")
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/tests/",
                json={"code": "def foo():"},
            )
    assert response.status_code == 503


@pytest.mark.asyncio
async def test_docs_gen_llm_error():
    with patch("app.services.llm.generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = RuntimeError("LLM unavailable")
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/docs/",
                json={"code": "def foo():"},
            )
    assert response.status_code == 503


@pytest.mark.asyncio
async def test_completion_stream():
    async def fake_stream(prompt: str, model: str | None = None):
        yield "    return "
        yield "x + y"

    with patch("app.services.llm.generate_stream", new=fake_stream):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/completion/",
                json={"code": "def add(x, y):", "stream": True},
            )
    assert response.status_code == 200
    assert b"return" in response.content


def test_strip_fences_plain_text():
    assert strip_fences("hello world") == "hello world"


def test_strip_fences_bare_fence():
    text = "```\nprint('hi')\n```"
    assert strip_fences(text) == "print('hi')"


def test_strip_fences_language_fence():
    text = "```python\nprint('hi')\n```"
    assert strip_fences(text) == "print('hi')"


@pytest.mark.parametrize("endpoint", ["/completion/", "/tests/", "/docs/"])
@pytest.mark.asyncio
async def test_missing_code_returns_422(endpoint):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(endpoint, json={"language": "python"})
    assert response.status_code == 422
