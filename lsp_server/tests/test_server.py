from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from lsprotocol.types import CompletionParams, Position, TextDocumentIdentifier


@pytest.fixture
def mock_ls():
    ls = MagicMock()
    doc = MagicMock()
    doc.source = "def add(x, y):"
    ls.workspace.get_document.return_value = doc
    return ls


@pytest.fixture
def completion_params():
    return CompletionParams(
        text_document=TextDocumentIdentifier(uri="file:///test.py"),
        position=Position(line=0, character=15),
    )


@pytest.mark.asyncio
async def test_completions_returns_list(mock_ls, completion_params, monkeypatch):
    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value={"suggestion": "    return x + y"})
    mock_response.raise_for_status = MagicMock()

    import server

    monkeypatch.setattr(server._http_client, "post", AsyncMock(return_value=mock_response))

    result = await server.completions(mock_ls, completion_params)

    assert result is not None
    assert len(result.items) == 1
    assert result.items[0].insert_text == "    return x + y"


@pytest.mark.asyncio
async def test_completions_on_backend_error(mock_ls, completion_params, monkeypatch):
    import server

    monkeypatch.setattr(
        server._http_client,
        "post",
        AsyncMock(side_effect=httpx.ConnectError("connection refused")),
    )

    result = await server.completions(mock_ls, completion_params)

    assert result.items == []


@pytest.mark.asyncio
async def test_completions_sends_python_language(mock_ls, monkeypatch):
    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value={"suggestion": "x"})
    mock_response.raise_for_status = MagicMock()

    import server

    post = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(server._http_client, "post", post)

    params = CompletionParams(
        text_document=TextDocumentIdentifier(uri="file:///test.py"),
        position=Position(line=0, character=0),
    )
    await server.completions(mock_ls, params)

    assert post.call_args.kwargs["json"]["language"] == "python"


@pytest.mark.asyncio
async def test_completions_sends_unknown_language(mock_ls, monkeypatch):
    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value={"suggestion": "x"})
    mock_response.raise_for_status = MagicMock()

    import server

    post = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(server._http_client, "post", post)

    params = CompletionParams(
        text_document=TextDocumentIdentifier(uri="file:///notes.txt"),
        position=Position(line=0, character=0),
    )
    await server.completions(mock_ls, params)

    assert post.call_args.kwargs["json"]["language"] == "unknown"
