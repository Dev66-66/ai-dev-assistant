from openai import AsyncOpenAI

from app.config import settings

_client = AsyncOpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)


async def generate(prompt: str) -> str:
    response = await _client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


async def generate_stream(prompt: str):
    stream = await _client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
