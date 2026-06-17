import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings
from app.services import llm
from app.services.text import strip_fences

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/completion", tags=["completion"])

_completion_model = settings.ollama_completion_model if settings.llm_provider == "ollama" else None


class CompletionRequest(BaseModel):
    code: str
    language: str = "python"
    cursor_line: int = 0
    stream: bool = False


class CompletionResponse(BaseModel):
    suggestion: str


PROMPT_TEMPLATE = """\
You are an expert {language} programmer. Complete the following code snippet.
Return ONLY the code continuation, no explanations, no markdown fences.

Code so far:
{code}

Continue from where it left off:"""


@router.post("/", response_model=CompletionResponse)
async def get_completion(req: CompletionRequest):
    prompt = PROMPT_TEMPLATE.format(language=req.language, code=req.code)

    if req.stream:
        try:
            source = llm.generate_stream(prompt, model=_completion_model)
        except Exception:
            logger.exception("LLM streaming completion failed")
            raise HTTPException(status_code=503, detail="LLM service unavailable")

        async def safe_stream():
            try:
                async for chunk in source:
                    yield chunk
            except Exception:
                logger.exception("LLM streaming completion failed during iteration")

        return StreamingResponse(safe_stream(), media_type="text/plain")

    try:
        suggestion = await llm.generate(prompt, max_tokens=80, model=_completion_model)
    except Exception:
        logger.exception("LLM completion failed")
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    return CompletionResponse(suggestion=strip_fences(suggestion))
