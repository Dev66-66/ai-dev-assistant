from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.gemini import generate, generate_stream

router = APIRouter(prefix="/completion", tags=["completion"])


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
        return StreamingResponse(
            generate_stream(prompt),
            media_type="text/plain",
        )

    suggestion = await generate(prompt)
    return CompletionResponse(suggestion=suggestion.strip())
