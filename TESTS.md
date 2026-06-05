# Описание тестов

## Backend — `backend/tests/test_api.py`

Тесты используют `httpx.AsyncClient` с `ASGITransport` — это позволяет обращаться к
FastAPI-приложению напрямую в памяти, без запуска реального HTTP-сервера.
Все вызовы к LLM изолированы фикстурой `mock_generate`, которая подменяет
`app.services.gemini.generate` через `unittest.mock.patch`.

### Фикстура `mock_generate`

```python
@pytest.fixture
def mock_generate():
    with patch("app.services.gemini.generate", new_callable=AsyncMock) as m:
        yield m
```

Патчит функцию `generate` на уровне модуля сервиса. Тесты, принимающие эту фикстуру,
управляют возвращаемым значением через `mock_generate.return_value` и не делают реальных
запросов к OpenRouter / Ollama.

---

### `test_health`

**Что проверяет:** эндпоинт `GET /health` возвращает HTTP 200 и тело `{"status": "ok"}`.

**Как работает:** делает GET-запрос без фикстуры mock_generate (LLM не задействован),
проверяет статус и точное JSON-содержимое ответа.

---

### `test_ui_serves_html`

**Что проверяет:** эндпоинт `GET /` отдаёт HTML-страницу (Web UI).

**Как работает:** делает GET-запрос, проверяет HTTP 200 и наличие `text/html`
в заголовке `Content-Type`. Убеждается, что статические файлы смонтированы корректно.

---

### `test_completion`

**Что проверяет:** эндпоинт `POST /completion/` возвращает HTTP 200 и поле `suggestion`
в ответе при корректном запросе с явным указанием языка.

**Как работает:** `mock_generate` возвращает `"    return x + y"`. Отправляет запрос
`{"code": "def add(x, y):", "language": "python"}`, проверяет статус и наличие ключа
`suggestion` в JSON-ответе.

---

### `test_completion_default_language`

**Что проверяет:** эндпоинт `POST /completion/` работает корректно, если параметр
`language` не передан (используется значение по умолчанию `"python"`).

**Как работает:** `mock_generate` возвращает `"    pass"`. Отправляет запрос только
с полем `code`, проверяет HTTP 200. Верифицирует, что Pydantic-модель корректно
применяет дефолтные значения.

---

### `test_tests_gen`

**Что проверяет:** эндпоинт `POST /tests/` возвращает HTTP 200 и поле `tests`
в ответе.

**Как работает:** `mock_generate` возвращает строку с pytest-тестом. Отправляет
запрос с простой функцией `add`, проверяет статус и наличие ключа `tests` в ответе.

---

### `test_docs_gen`

**Что проверяет:** эндпоинт `POST /docs/` возвращает HTTP 200 и поле `docstring`
в ответе при запросе без явного указания стиля (используется `"google"` по умолчанию).

**Как работает:** `mock_generate` возвращает текст докстринга. Проверяет статус
и наличие ключа `docstring` в JSON-ответе.

---

### `test_docs_gen_with_style`

**Что проверяет:** эндпоинт `POST /docs/` корректно принимает параметр `style`
и возвращает непустой докстринг.

**Как работает:** `mock_generate` возвращает numpy-style докстринг. Отправляет запрос
с `{"style": "numpy"}`, проверяет HTTP 200 и что поле `docstring` не пустое.
Верифицирует, что параметр `style` проходит через роутер без ошибок.

---

## LSP-сервер — `lsp_server/tests/test_server.py`

Тесты проверяют обработчик `completions` LSP-сервера. Вся HTTP-коммуникация с backend
изолирована через `unittest.mock.patch("httpx.AsyncClient")`.

### Фикстура `mock_ls`

Создаёт mock-объект языкового сервера (`LanguageServer`) с подключённым документом,
содержащим текст `"def add(x, y):"`. Используется как первый аргумент обработчика.

### Фикстура `completion_params`

Создаёт объект `CompletionParams` с URI `file:///test.py` и позицией курсора
`(line=0, character=15)` — имитирует LSP-запрос на автодополнение.

---

### `test_completions_returns_list`

**Что проверяет:** при успешном ответе backend обработчик `completions` возвращает
непустой (или пустой) `CompletionList` без исключений.

**Как работает:** полностью мокает `httpx.AsyncClient` как async context manager,
настраивает `client.post` на возврат mock-ответа с `{"suggestion": "    return x + y"}`.
Импортирует и вызывает функцию `completions` напрямую. Проверяет, что результат не `None`
и является `CompletionList`.

---

### `test_completions_on_backend_error`

**Что проверяет:** ключевое свойство отказоустойчивости — при любой сетевой ошибке
или недоступности backend LSP-сервер возвращает пустой список подсказок, а не
бросает исключение.

**Как работает:** настраивает `client.post` на выброс `Exception("connection refused")`.
Проверяет, что `result.items == []`. Гарантирует, что редактор продолжает работать
при недоступном backend.

---

## Запуск тестов

```bash
# Backend (из папки backend/)
pytest tests/ -v --cov=app --cov-report=term-missing

# LSP-сервер (из папки lsp_server/)
pytest tests/ -v
```

## Покрытие

| Компонент | Тестов | Покрытие |
|---|---|---|
| Backend | 7 | 90% |
| LSP Server | 2 | — |
