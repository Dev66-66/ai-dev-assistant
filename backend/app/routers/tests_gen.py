from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import llm

router = APIRouter(prefix="/tests", tags=["tests"])


class TestGenRequest(BaseModel):
    code: str
    language: str = "python"
    framework: str = "pytest"


class TestGenResponse(BaseModel):
    tests: str


PROMPT_TEMPLATE = """\
You are an expert {language} developer. Write {framework} unit tests for the following code.
Cover happy path, edge cases, and error cases.
Return ONLY the test code, no explanations, no markdown fences.

Code to test:
{code}

Tests:"""


def _strip_fences(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


@router.post("/", response_model=TestGenResponse)
async def generate_tests(req: TestGenRequest) -> TestGenResponse:
    prompt = PROMPT_TEMPLATE.format(language=req.language, framework=req.framework, code=req.code)
    try:
        tests = await llm.generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    return TestGenResponse(tests=_strip_fences(tests))
