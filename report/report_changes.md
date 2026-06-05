# Что нужно изменить в report_fomichev.md

Список изменений, вызванных переходом с Google Gemini API на OpenRouter + Ollama,
добавлением постобработки ответов (`_strip_fences`) и оптимизацией autocomplete.

---

## Оглавление

**Пункт 3.4** — переименовать:
> ~~3.4 Выбор Google Gemini API~~ → **3.4 Выбор LLM провайдера**

---

## Введение (стр. 4)

**Абзац 4:**
> ~~"центральный backend-сервис на Python взаимодействует с Google Gemini API"~~

→ "центральный backend-сервис на Python взаимодействует с LLM через унифицированный OpenAI-совместимый интерфейс, поддерживая как облачный провайдер OpenRouter, так и локальный запуск моделей через Ollama"

**Цель проекта:**
> ~~"на основе большой языковой модели Gemini"~~

→ "на основе больших языковых моделей с поддержкой локального (Ollama) и облачного (OpenRouter) режимов работы"

**Задача в списке:**
> ~~"реализовать интеграцию с Google Gemini API для генерации кода"~~

→ "реализовать интеграцию с LLM через OpenAI-совместимый API с поддержкой провайдеров OpenRouter и Ollama"

---

## 1.4 Большие языковые модели в задачах генерации кода

**Абзац про модель:**
> ~~"В данном проекте используется модель **Google Gemini 2.0 Flash**..."~~
> ~~"Gemini 2.0 Flash обеспечивает высокое качество..."~~

→ "В данном проекте поддерживаются два режима работы с LLM. В облачном режиме используется провайдер **OpenRouter** — агрегатор моделей с единым OpenAI-совместимым API, по умолчанию модель `google/gemma-4-31b-it:free`. В локальном режиме используется **Ollama** — инструмент для запуска open-source моделей непосредственно на машине разработчика, по умолчанию модель `qwen2.5-coder:7b` для генерации тестов и документации и `qwen2.5-coder:1.5b` для автодополнения кода. Локальный режим обеспечивает полную конфиденциальность: код не покидает рабочую машину."

**Про `GEMINI_MODEL`:**
> ~~"Модель конфигурируема через переменную окружения `GEMINI_MODEL`"~~

→ "Провайдер и модель конфигурируются через переменные окружения `LLM_PROVIDER`, `OPENROUTER_MODEL` и `OLLAMA_MODEL`, что позволяет переключаться между режимами без изменения кода."

---

## 1.5 Анализ аналогов — Таблица 1.1

**Строка «Модель»:**
> ~~"Google Gemini 2.0 Flash"~~

→ "OpenRouter / Ollama (конфигурируемо)"

**Строка «Передача кода»:**
> ~~"По выбору пользователя"~~ (уже верно, но уточнить)

→ "Нет (Ollama) / Да (OpenRouter)"

---

## 2.2 Общая архитектура системы

**Диаграмма — нижний блок:**
```
было:
│ google-generativeai SDK
└── Google Gemini API (gemini-2.0-flash model)

стало:
│ openai SDK (OpenAI-compatible)
└── OpenRouter API  ──или──  Ollama (локально)
```

**Описание взаимодействия** — заменить все упоминания Gemini API на LLM провайдер.

---

## 2.3 Архитектура backend-сервиса

**Комментарий к файлу в структуре:**
> ~~"services/gemini.py — Клиент Google Gemini API"~~

→ "services/gemini.py — LLM клиент (OpenRouter или Ollama, openai SDK)"

**Описание сервисного слоя:**
> ~~"содержит единственный модуль `gemini.py`, инкапсулирующий всё взаимодействие с Gemini API"~~

→ "содержит единственный модуль `gemini.py`, инкапсулирующий взаимодействие с LLM через OpenAI-совместимый интерфейс. Конкретный провайдер (OpenRouter или Ollama) выбирается при старте приложения на основе переменной `LLM_PROVIDER`."

---

## 2.6 Потоки данных — Сценарий 1 (Inline completion)

**Диаграмма:**
> ~~"gemini.generate(prompt)"~~
> ~~"google-generativeai SDK"~~
> ~~"Gemini API → response.text"~~

→
```
gemini.generate(prompt, max_tokens=80, model=_completion_model)
        ↓ openai SDK (OpenAI-compatible)
OpenRouter API / Ollama → response.choices[0].message.content
        ↓ _strip_fences()
CompletionResponse {suggestion: str}
```

**Сценарии 2 и 3** — аналогично заменить `gemini.generate(prompt)` и убрать упоминание Gemini.

---

## 3.1 Выбор языка программирования backend

**Абзац:**
> ~~"Все ведущие провайдеры языковых моделей, включая Google (Gemini)... предоставляют официальные Python SDK"~~
> ~~"Использование Python позволяет применять официальную библиотеку `google-generativeai`"~~

→ "OpenAI-совместимый протокол, реализованный в библиотеке `openai`, поддерживается широким кругом провайдеров, включая OpenRouter и Ollama, что обеспечивает гибкость выбора модели без изменения кода."

---

## 3.4 Выбор LLM провайдера *(переименованный раздел)*

Раздел полностью переписать. Структура нового раздела:

**Было:** описание Google Gemini API, `google-generativeai` SDK, `GEMINI_API_KEY`.

**Стало:** описать двух провайдеров:

1. **OpenRouter** — облачный агрегатор с OpenAI-совместимым API (`openai` SDK, `base_url=https://openrouter.ai/api/v1`). Преимущества: единый ключ для сотен моделей, бесплатный tier, надёжность.

2. **Ollama** — локальный инференс open-source моделей. Также OpenAI-совместимый API (`base_url=http://localhost:11434/v1`, `api_key="ollama"`). Преимущества: конфиденциальность, отсутствие затрат на токены, работа без интернета.

3. **Архитектурное решение** — провайдер выбирается через `LLM_PROVIDER` в `.env`, клиент инициализируется единожды при старте, остальной код не меняется.

4. **Оптимизация autocomplete** — для inline completion используется `qwen2.5-coder:1.5b` (`OLLAMA_COMPLETION_MODEL`) и ограничение `max_tokens=80`, что ускоряет ответ в 4–5 раз по сравнению с 7B моделью.

---

## 4.1 Backend: конфигурация — Листинг 4.1 (config.py)

Заменить листинг на актуальный:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_provider: str = "openrouter"  # "openrouter" or "ollama"

    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemma-4-31b-it:free"

    ollama_base_url: str = "http://host.docker.internal:11434/v1"
    ollama_model: str = "qwen2.5-coder:7b"
    ollama_completion_model: str = "qwen2.5-coder:1.5b"

    backend_host: str = "0.0.0.0"  # nosec B104
    backend_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
```

**Пояснение под листингом** — заменить описание `gemini_api_key` как fail-fast поля на описание `llm_provider` как переключателя провайдера.

---

## 4.2 Сервис взаимодействия с LLM *(переименовать)*

> ~~"4.2 Сервис взаимодействия с Gemini API"~~

→ **"4.2 Сервис взаимодействия с LLM"**

**Листинг 4.3 (gemini.py)** — заменить на актуальный:

```python
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
```

**Пояснение** — обновить: описать условную инициализацию клиента, параметры `max_tokens` и `model`, OpenAI-совместимый интерфейс.

---

## 4.3 Роутер дополнения кода — Листинг 4.4 (completion.py)

Заменить на актуальный (добавлены `_strip_fences`, `_completion_model`, `max_tokens=80`):

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings
from app.services import gemini

router = APIRouter(prefix="/completion", tags=["completion"])

_completion_model = settings.ollama_completion_model if settings.llm_provider == "ollama" else None

# ... (CompletionRequest, CompletionResponse, PROMPT_TEMPLATE без изменений)

def _strip_fences(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


@router.post("/", response_model=CompletionResponse)
async def get_completion(req: CompletionRequest):
    prompt = PROMPT_TEMPLATE.format(language=req.language, code=req.code)
    if req.stream:
        return StreamingResponse(gemini.generate_stream(prompt), media_type="text/plain")
    try:
        suggestion = await gemini.generate(prompt, max_tokens=80, model=_completion_model)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    return CompletionResponse(suggestion=_strip_fences(suggestion))
```

**Пояснение** — добавить абзац про `_strip_fences` (удаление markdown-оберток, характерных для локальных моделей) и про `max_tokens=80` и отдельную модель для autocomplete.

---

## 4.4 Роутер генерации тестов — Листинг 4.5 (tests_gen.py)

Добавить `_strip_fences` в листинг и вызов `_strip_fences(tests)` вместо `tests.strip()`.

---

## 4.5 Роутер генерации документации — Листинг 4.6 (docs_gen.py)

Обновить листинг: новый `PROMPT_TEMPLATE` с примером корректного вывода + функция `_strip_fences` + вызов `_strip_fences(docstring)`.

---

## 5.1 Общая организация тестирования

**Абзац об изоляции:**
> ~~"Все вызовы к Google Gemini API заменяются mock-объектами."~~

→ "Все вызовы к LLM (OpenRouter / Ollama) заменяются mock-объектами."

---

## 5.2 Модульное тестирование — Листинг 5.1 (conftest.py)

Заменить листинг:

```python
import os

# Set dummy env vars before any app module is imported.
# This prevents pydantic-settings from raising ValidationError
# when OPENROUTER_API_KEY is absent in the local environment.
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-not-used")
os.environ.setdefault("OPENROUTER_MODEL", "google/gemini-2.0-flash")
```

---

## Заключение

**Пункт 3:**
> ~~"интегрированный с Google Gemini API через официальный Python SDK"~~

→ "интегрированный с LLM через OpenAI-совместимый интерфейс с поддержкой провайдеров OpenRouter (облако) и Ollama (локально)"

**Направления дальнейшего развития** — удалить пункт:
> ~~"интеграция с локальными LLM через Ollama..."~~ — **уже реализовано**

Заменить на:
> "оптимизация промптов и тонкая настройка локальных моделей для повышения качества генерации"

---

## Список использованной литературы

**Источник 6** — заменить/дополнить:
> ~~"Google. Gemini API Documentation"~~

Добавить:
> OpenRouter Documentation [Электронный ресурс]. — URL: https://openrouter.ai/docs
> Ollama Documentation [Электронный ресурс]. — URL: https://ollama.com/docs

---

## Приложение А — Полные листинги

Обновить **все** листинги в соответствии с изменениями разделов 4.1–4.5:

| Листинг | Файл | Что изменить |
|---|---|---|
| А.1 | config.py | Новые поля: `llm_provider`, `openrouter_*`, `ollama_*` |
| А.3 | services/gemini.py | Заменить целиком на openai SDK клиент |
| А.4 | routers/completion.py | Добавить `_strip_fences`, `_completion_model`, `max_tokens=80` |
| А.5 | routers/tests_gen.py | Добавить `_strip_fences` |
| А.6 | routers/docs_gen.py | Новый промпт + `_strip_fences` |
| А.7 | tests/conftest.py | `GEMINI_*` → `OPENROUTER_*` |

---

## Приложение Б — LSP-сервер

**Листинг Б.1 (server.py)** — строка с документацией CompletionItem:
> ~~`documentation="Generated by Gemini"`~~

→ `documentation="Generated by AI Dev Assistant"`

---

## Приложение В — VS Code расширение

**Листинг В.5 (package.json)** — описание расширения:
> ~~`"description": "AI-powered code completion, test and doc generation via Gemini"`~~

→ `"description": "AI-powered code completion, test and doc generation via OpenRouter or Ollama"`
