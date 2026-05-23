from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import completion, tests_gen, docs_gen

app = FastAPI(
    title="AI Dev Assistant API",
    description="LLM-powered backend for code completion, test and doc generation",
    version="0.1.0",
)

app.include_router(completion.router)
app.include_router(tests_gen.router)
app.include_router(docs_gen.router)

_static = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=_static), name="static")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def ui() -> FileResponse:
    return FileResponse(_static / "index.html")
