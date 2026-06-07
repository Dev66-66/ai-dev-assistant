from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import llm

router = APIRouter(prefix="/docs", tags=["docs"])


class DocsGenRequest(BaseModel):
    code: str
    language: str = "python"
    style: str = "google"


class DocsGenResponse(BaseModel):
    docstring: str


PROMPT_TEMPLATE = """\
You are an expert {language} developer. Write a {style}-style docstring for the following function or class.
Return ONLY the docstring text itself — no triple quotes, no code fences, no markdown, no explanations.

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


def _strip_fences(text: str) -> str:
    """Remove markdown code fences if the model wrapped the output."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


@router.post("/", response_model=DocsGenResponse)
async def generate_docs(req: DocsGenRequest) -> DocsGenResponse:
    prompt = PROMPT_TEMPLATE.format(language=req.language, style=req.style, code=req.code)
    try:
        docstring = await llm.generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    return DocsGenResponse(docstring=_strip_fences(docstring))
