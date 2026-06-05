# AI Dev Assistant

[![CI](https://github.com/Dev66-66/ai-dev-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Dev66-66/ai-dev-assistant/actions/workflows/ci.yml)

AI-ассистент для разработчика с интеграцией в VS Code через Language Server Protocol.

## Возможности

- **Подсказки по коду** — inline completion через LSP
- **Генерация тестов** — автоматическое создание pytest-тестов
- **Генерация документации** — docstring для функций и классов
- **Web UI** — браузерный интерфейс для быстрого тестирования без IDE
- **Локальный запуск** — поддержка Ollama для полной конфиденциальности кода

## Архитектура

```
VS Code Extension (TypeScript)
        │ LSP Protocol (TCP :2087)
LSP Server (Python + pygls)
        │ HTTP/REST
FastAPI Backend (Python)        ←── Web UI (/)
        │
  OpenRouter API  ──или──  Ollama (локально)
```

## Стек технологий

| Компонент | Технологии |
|-----------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic V2 |
| LLM (облако) | [OpenRouter](https://openrouter.ai) (`google/gemma-4-31b-it:free` по умолчанию) |
| LLM (локально) | [Ollama](https://ollama.com) (`qwen2.5-coder:7b` по умолчанию) |
| LSP Server | Python, pygls 1.3.1 |
| VS Code Extension | TypeScript, vscode-languageclient 9 |
| Контейнеризация | Docker, Docker Compose |
| Качество кода | ruff, bandit, pytest-cov |

## Установка VS Code расширения

В репозитории есть готовый файл `vscode-extension/ai-dev-assistant-0.1.0.vsix` — это собранное расширение для VS Code, которое не требует компиляции.

**Установка:**

1. Скачать репозиторий (или только файл `.vsix`)
2. Открыть VS Code → `Extensions` (Ctrl+Shift+X)
3. Нажать `...` → `Install from VSIX...`
4. Выбрать файл `vscode-extension/ai-dev-assistant-0.1.0.vsix`
5. Перезагрузить окно (`Ctrl+Shift+P` → `Developer: Reload Window`)

После установки при открытии любого `.py` файла:
- В правом верхнем углу редактора появятся кнопки **⚗ Generate Tests** и **📖 Generate Docstring**
- При наборе кода через ~1.5 секунды появляется AI-подсказка серым текстом — принять через **Tab**

> Расширение требует запущенного бэкенда (`docker compose up`)

## Быстрый старт

### Вариант А — OpenRouter (облако)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Dev66-66/ai-dev-assistant.git
cd ai-dev-assistant

# 2. Настроить переменные окружения
cp .env.example .env
# Вставить OPENROUTER_API_KEY в .env  (получить на https://openrouter.ai/keys)
# Убедиться: LLM_PROVIDER=openrouter

# 3. Запустить через Docker Compose
docker compose up --build
```

### Вариант Б — Ollama (локально, без передачи кода в облако)

```bash
# 1. Установить Ollama: https://ollama.com/download
# 2. Скачать модель
ollama pull qwen2.5-coder:7b

# 3. Клонировать и настроить
git clone https://github.com/Dev66-66/ai-dev-assistant.git
cd ai-dev-assistant
cp .env.example .env
# Установить в .env: LLM_PROVIDER=ollama

# 4. Запустить
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
├── backend/            # FastAPI + LLM сервис (OpenRouter / Ollama)
├── lsp_server/         # Language Server (pygls)
├── vscode-extension/   # VS Code расширение (TypeScript)
└── .github/workflows/  # CI/CD pipeline
```

## Требования

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- OpenRouter API ключ ([openrouter.ai/keys](https://openrouter.ai/keys)) **или** [Ollama](https://ollama.com/download)
