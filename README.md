# AI Dev Assistant

[![CI](https://github.com/Dev66-66/ai-dev-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Dev66-66/ai-dev-assistant/actions/workflows/ci.yml)

AI-ассистент для разработчика с интеграцией в VS Code через Language Server Protocol.

## Возможности

- **Подсказки по коду** — inline completion через LSP
- **Генерация тестов** — автоматическое создание pytest-тестов
- **Генерация документации** — docstring для функций и классов
- **Web UI** — браузерный интерфейс для быстрого тестирования без IDE

## Архитектура

```
VS Code Extension (TypeScript)
        │ LSP Protocol (TCP :2087)
LSP Server (Python + pygls)
        │ HTTP/REST
FastAPI Backend (Python)        ←── Web UI (/)
        │
  Gemini API
```

## Стек технологий

| Компонент | Технологии |
|-----------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic V2 |
| LLM | Google Gemini API (`gemini-2.0-flash`) |
| LSP Server | Python, pygls 1.3.1 |
| VS Code Extension | TypeScript, vscode-languageclient 9 |
| Контейнеризация | Docker, Docker Compose |
| Качество кода | ruff, bandit, pytest-cov |

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Dev66-66/ai-dev-assistant.git
cd ai-dev-assistant

# 2. Настроить переменные окружения
cp .env.example .env
# Вставить GEMINI_API_KEY в .env  (получить на https://aistudio.google.com)

# 3. Запустить через Docker Compose
docker compose up --build
```

После запуска:
- **Web UI** → http://localhost:8000
- **API docs** → http://localhost:8000/docs
- **LSP Server** → TCP порт 2087

## Разработка

```bash
# Backend — установить зависимости и запустить тесты
cd backend
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v --cov=app

# LSP Server
cd lsp_server
pip install -r requirements.txt
python server.py

# VS Code Extension
cd vscode-extension
npm install
npm run compile
```

## Структура проекта

```
ai-dev-assistant/
├── backend/            # FastAPI + Gemini API сервис
├── lsp_server/         # Language Server (pygls)
├── vscode-extension/   # VS Code расширение (TypeScript)
└── .github/workflows/  # CI/CD pipeline
```

## Требования

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Gemini API ключ ([Google AI Studio](https://aistudio.google.com))
