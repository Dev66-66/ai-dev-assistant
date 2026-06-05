from openai import AsyncOpenAI

from app.config import settings

if settings.llm_provider == "ollama":
    _client = AsyncOpenAI(
        api_key="ollama",
        base_url=settings.ollama_base_url,
    )
    _model = settings.ollama_model
else:
    _client = AsyncOpenAI(
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
    )
    _model = settings.openrouter_model


async def generate(prompt: str, max_tokens: int | None = None, model: str | None = None) -> str:
    response = await _client.chat.completions.create(
        model=model or _model,
        messages=[{"role": "user", "content": prompt}],
        **({"max_tokens": max_tokens} if max_tokens is not None else {}),
    )
    return response.choices[0].message.content


async def generate_stream(prompt: str):
    stream = await _client.chat.completions.create(
        model=_model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
