import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import llm
from app.services.text import strip_fences

logger = logging.getLogger(__name__)

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


@router.post("/", response_model=TestGenResponse)
async def generate_tests(req: TestGenRequest) -> TestGenResponse:
    prompt = PROMPT_TEMPLATE.format(language=req.language, framework=req.framework, code=req.code)
    try:
        tests = await llm.generate(prompt)
    except Exception:
        logger.exception("LLM test generation failed")
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    return TestGenResponse(tests=strip_fences(tests))
