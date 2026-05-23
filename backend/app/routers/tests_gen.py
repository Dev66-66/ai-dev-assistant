from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini import generate

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
    prompt = PROMPT_TEMPLATE.format(
        language=req.language, framework=req.framework, code=req.code
    )
    tests = await generate(prompt)
    return TestGenResponse(tests=tests.strip())
