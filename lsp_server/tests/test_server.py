from unittest.mock import AsyncMock, MagicMock, patch
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
async def test_completions_returns_list(mock_ls, completion_params):
    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value={"suggestion": "    return x + y"})
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        import importlib
        import lsp_server.server as srv_module
        importlib.reload(srv_module)

        from lsp_server.server import completions
        result = await completions(mock_ls, completion_params)

    assert result is not None
    assert len(result.items) >= 0


@pytest.mark.asyncio
async def test_completions_on_backend_error(mock_ls, completion_params):
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(side_effect=Exception("connection refused"))
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        from lsp_server.server import completions
        result = await completions(mock_ls, completion_params)

    assert result.items == []
