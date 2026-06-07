from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings
from app.services import llm

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


def _strip_fences(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


@router.post("/", response_model=CompletionResponse)
async def get_completion(req: CompletionRequest):
    prompt = PROMPT_TEMPLATE.format(language=req.language, code=req.code)

    if req.stream:
        return StreamingResponse(
            llm.generate_stream(prompt),
            media_type="text/plain",
        )

    try:
        suggestion = await llm.generate(prompt, max_tokens=80, model=_completion_model)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    return CompletionResponse(suggestion=_strip_fences(suggestion))
