from fastapi import FastAPI
from app.routers import completion, tests_gen, docs_gen

app = FastAPI(
    title="AI Dev Assistant API",
    description="LLM-powered backend for code completion, test and doc generation",
    version="0.1.0",
)

app.include_router(completion.router)
app.include_router(tests_gen.router)
app.include_router(docs_gen.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
