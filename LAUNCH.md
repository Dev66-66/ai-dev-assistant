# Инструкция по запуску AI Dev Assistant

## Предварительные требования

| Компонент | Версия | Проверка |
|---|---|---|
| Python | 3.12+ | `python --version` |
| Node.js | 20+ | `node --version` |
| Docker Desktop | любая | `docker --version` |
| Gemini API ключ | — | [aistudio.google.com](https://aistudio.google.com) |

> **Gemini API ключ:** зайди на https://aistudio.google.com → Get API key → скопируй.

---

## Шаг 1 — Настройка окружения

```bash
cd D:\ai-dev-assistant
copy .env.example .env
```

Открой `.env` и вставь ключ:

```
GEMINI_API_KEY=AIza_твой_ключ_здесь
GEMINI_MODEL=gemini-2.0-flash
BACKEND_PORT=8000
LSP_PORT=2087
```

---

## Способ А — Docker Compose (рекомендуется)

```bash
docker compose up --build
```

После запуска:

| Адрес | Что |
|---|---|
| http://localhost:8000 | Web UI (3 вкладки: подсказки / тесты / документация) |
| http://localhost:8000/docs | Swagger API документация |
| TCP :2087 | LSP Server (для VS Code расширения) |

Остановка:
```bash
docker compose down
```

---

## Способ Б — Без Docker (два терминала)

### Терминал 1 — Backend

```powershell
cd D:\ai-dev-assistant\backend
pip install -r requirements.txt

$env:GEMINI_API_KEY="AIza_твой_ключ"
$env:GEMINI_MODEL="gemini-2.0-flash"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Убедись что сервер запустился: http://localhost:8000/health → `{"status":"ok"}`

### Терминал 2 — LSP Server

```powershell
cd D:\ai-dev-assistant\lsp_server
pip install -r requirements.txt

$env:BACKEND_URL="http://localhost:8000"
$env:LSP_HOST="0.0.0.0"
$env:LSP_PORT="2087"

python server.py
```

---

## Шаг 2 — Расширение VS Code

### Сборка (один раз)

```powershell
cd D:\ai-dev-assistant\vscode-extension
npm install
npm run compile
```

### Запуск в режиме разработки

1. Открой VS Code в папке `vscode-extension`:
   ```
   code D:\ai-dev-assistant\vscode-extension
   ```
2. Нажми **F5** — откроется окно **Extension Development Host**
3. В этом окне открой любой `.py` файл

### Доступные команды (Ctrl+Shift+P → введи "AI:")

| Команда | Действие |
|---|---|
| **AI: Generate Tests** | Выдели код → генерирует pytest-тесты в соседней вкладке |
| **AI: Generate Docstring** | Выдели функцию/класс → вставляет docstring перед ней |

Inline-подсказки работают автоматически при наборе кода.

---

## Быстрая проверка без VS Code

Открой http://localhost:8000 в браузере — Web UI с тремя вкладками.

Или через curl:

```bash
# Подсказка по коду
curl -X POST http://localhost:8000/completion/ \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(x, y):", "language": "python"}'

# Генерация тестов
curl -X POST http://localhost:8000/tests/ \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(x, y):\n    return x + y"}'

# Генерация docstring
curl -X POST http://localhost:8000/docs/ \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(x, y):\n    return x + y"}'
```

---

## Запуск тестов

```bash
# Backend
cd D:\ai-dev-assistant\backend
pip install -r requirements-dev.txt
pytest tests/ -v --cov=app

# LSP Server
cd D:\ai-dev-assistant\lsp_server
pytest tests/ -v
```

---

## Решение проблем

| Проблема | Решение |
|---|---|
| `GEMINI_API_KEY` не задан | Проверь `.env` файл, он должен быть рядом с `docker-compose.yml` |
| Порт 8000 занят | Измени `BACKEND_PORT=8001` в `.env` |
| LSP не подключается | Убедись что backend запущен раньше LSP server |
| Extension не видит команды | Убедись что в Extension Development Host открыт `.py` файл |
