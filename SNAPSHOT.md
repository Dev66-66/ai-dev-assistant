# Снимок состояния проекта #9
**Дата:** 2026-06-05
**Репозиторий:** https://github.com/Dev66-66/ai-dev-assistant
**Ветка:** master
**Последний коммит:** `8286e7e docs: add TESTS.md with description of all tests`

## Полный список выполненного

- [x] Scaffold + docker-compose + .env.example
- [x] Backend: FastAPI, 3 эндпоинта + стриминг + Web UI (GET /)
- [x] LSP Server: pygls, TCP 2087, Dockerfile
- [x] VS Code Extension: TypeScript, LSP клиент, 2 команды
- [x] CI/CD: lint + test(coverage 90%) + test-lsp + SAST — все джобы зелёные
- [x] conftest.py — тесты работают без реального API ключа
- [x] 7 тестов backend, 2 теста LSP server
- [x] README с CI badge
- [x] LAUNCH.md — инструкция по запуску (Docker / без Docker / VS Code)
- [x] Отчёт: полный, разделы 1–5 + Заключение + Литература + Приложения
- [x] report.docx сконвертирован
- [x] Миграция с Gemini API на OpenRouter (openai SDK, модель `google/gemma-4-31b-it:free`)
- [x] Поддержка Ollama — локальный запуск моделей, переключение через `LLM_PROVIDER` в `.env`
- [x] Постобработка ответов LLM — `_strip_fences()` во всех трёх роутерах
- [x] Оптимизация autocomplete — `qwen2.5-coder:1.5b` + `max_tokens=80` для скорости
- [x] История git очищена от сторонних подписей в коммитах
- [x] TESTS.md — локальное описание всех 9 тестов (gitignored)

## Исправленные баги CI

| Коммит | Проблема | Решение |
|---|---|---|
| `66d2a96` | bandit B104 exit 1 | `# nosec B104` с обоснованием |
| `c2016c4` | ModuleNotFoundError lsp tests | `from server import` вместо `from lsp_server.server import` |
| `53948c1` | Mock не перехватывал Gemini | `from app.services import gemini` → `gemini.generate()` |
| `1cfd780` | ruff I001, F401 | `ruff check --fix` |
| `a234f1e` | ruff format | `ruff format` |

## История миграции провайдера

| Дата | Провайдер | Причина |
|---|---|---|
| до 2026-06-05 | Google Gemini API (прямой) | — |
| 2026-06-05 | OpenRouter (`google/gemma-4-31b-it:free`) | Превышение квоты Gemini free tier |
| 2026-06-05 | Ollama (`qwen2.5-coder:7b`) + OpenRouter | Требование ТЗ: локальный запуск для конфиденциальности |

## Конфигурация LLM (текущая)

| Параметр | Значение | Назначение |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | Активный провайдер |
| `OLLAMA_MODEL` | `qwen2.5-coder:7b` | Генерация тестов и документации |
| `OLLAMA_COMPLETION_MODEL` | `qwen2.5-coder:1.5b` | Inline autocomplete (быстрый) |
| `OPENROUTER_MODEL` | `google/gemma-4-31b-it:free` | Резерв при `LLM_PROVIDER=openrouter` |

## Локальные файлы (gitignored)

| Файл | Описание |
|---|---|
| `SNAPSHOT.md` | Этот файл |
| `TESTS.md` | Описание всех тестов — что проверяют и как работают |
| `report/` | Отчёт, docx, перечень правок |
| `.env` | Реальные ключи и конфигурация |

## Структура проекта

```
D:\ai-dev-assistant\
├── .github/workflows/ci.yml     # CI: lint + test + test-lsp + sast
├── .env.example                  # шаблон переменных окружения
├── docker-compose.yml
├── ruff.toml
├── LAUNCH.md                     # инструкция по запуску
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI + статика
│   │   ├── config.py            # Pydantic Settings (LLM_PROVIDER + оба провайдера)
│   │   ├── static/index.html    # Web UI
│   │   ├── routers/             # completion, tests_gen, docs_gen (все со _strip_fences)
│   │   └── services/gemini.py   # LLM клиент: OpenRouter или Ollama (openai SDK)
│   ├── tests/
│   │   ├── conftest.py          # env stub для локального запуска
│   │   └── test_api.py          # 7 тестов
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── Dockerfile
├── lsp_server/
│   ├── server.py
│   ├── tests/test_server.py     # 2 теста
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── Dockerfile
├── vscode-extension/
│   ├── src/
│   │   ├── extension.ts
│   │   ├── lspClient.ts
│   │   └── commands.ts
│   ├── package.json
│   └── tsconfig.json
└── report/                       # локальная папка (gitignored)
```

## Что осталось (опционально)

- [ ] Redis кэш ответов
- [ ] RAG по кодовой базе проекта

## Как возобновить работу

1. Прочитать этот файл
2. `git log --oneline` — проверить актуальный коммит
3. Запустить Ollama: `ollama serve` (если не запущена)
4. Запустить Docker: `docker compose up -d`
5. Продолжить с раздела "Что осталось"
