from fastapi import APIRouter
from pydantic import BaseModel

from app.services import gemini

router = APIRouter(prefix="/docs", tags=["docs"])


class DocsGenRequest(BaseModel):
    code: str
    language: str = "python"
    style: str = "google"


class DocsGenResponse(BaseModel):
    docstring: str


PROMPT_TEMPLATE = """\
You are an expert {language} developer. Write a {style}-style docstring for the following function or class.
Return ONLY the docstring content (without the triple quotes), no explanations.

Code:
{code}

Docstring:"""


@router.post("/", response_model=DocsGenResponse)
async def generate_docs(req: DocsGenRequest) -> DocsGenResponse:
    prompt = PROMPT_TEMPLATE.format(language=req.language, style=req.style, code=req.code)
    docstring = await gemini.generate(prompt)
    return DocsGenResponse(docstring=docstring.strip())
