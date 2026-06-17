import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import llm
from app.services.text import strip_fences

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/docs", tags=["docs"])


class DocsGenRequest(BaseModel):
    code: str
    language: str = "python"
    style: str = "google"


class DocsGenResponse(BaseModel):
    docstring: str


PROMPT_TEMPLATE = """\
You are an expert {language} developer. Write a {style}-style docstring \
for the following function or class.
Return ONLY the docstring text itself — no triple quotes, no code fences, \
no markdown, no explanations.

Example of correct output:
Adds two numbers.

Args:
    x: First number.
    y: Second number.

Returns:
    The sum of x and y.

Code:
{code}

Docstring:"""


@router.post("/", response_model=DocsGenResponse)
async def generate_docs(req: DocsGenRequest) -> DocsGenResponse:
    prompt = PROMPT_TEMPLATE.format(language=req.language, style=req.style, code=req.code)
    try:
        docstring = await llm.generate(prompt)
    except Exception:
        logger.exception("LLM docstring generation failed")
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    return DocsGenResponse(docstring=strip_fences(docstring))
