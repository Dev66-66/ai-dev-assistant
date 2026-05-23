# AI Dev Assistant

AI-ассистент для разработчика с интеграцией в VS Code через Language Server Protocol.

## Возможности

- **Подсказки по коду** — inline completion через LSP
- **Генерация тестов** — автоматическое создание pytest-тестов
- **Генерация документации** — docstring для функций и классов

## Архитектура

```
VS Code Extension (TypeScript)
        │ LSP Protocol
LSP Server (Python + pygls)
        │ HTTP/REST
FastAPI Backend (Python)
        │
  Gemini API
```

## Стек технологий

| Компонент | Технологии |
|-----------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic V2 |
| LLM | Google Gemini API |
| LSP Server | Python, pygls |
| VS Code Extension | TypeScript, vscode-languageclient |
| Контейнеризация | Docker, Docker Compose |

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/Dev66-66/ai-dev-assistant.git
cd ai-dev-assistant

# Настроить переменные окружения
cp .env.example .env
# Вставить GEMINI_API_KEY в .env

# Запустить через Docker Compose
docker compose up --build
```

## Разработка

Подробная документация по каждому компоненту — в соответствующих папках:

- [`backend/`](./backend/) — FastAPI сервис
- [`lsp_server/`](./lsp_server/) — LSP сервер
- [`vscode-extension/`](./vscode-extension/) — расширение VS Code

## Требования

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Gemini API ключ
