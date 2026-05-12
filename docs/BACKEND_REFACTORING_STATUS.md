# Оценка текущего рефакторинга бекенда

## Что уже реализовано

### 1. Слой представления (web_server.py)
- ✅ `web_server.py` принимает HTTP-запросы через `BaseHTTPRequestHandler`
- ✅ Парсит JSON в `do_POST`
- ✅ Маршрутизует запросы через `match self.path`
- ✅ Отправляет JSON-ответы через `_send_response`
- ✅ Раздаёт статические файлы из `static/` через `serve_static_file`

### 2. Слой доступа к данным
- ✅ `data/db_connector.py` абстрагирует выбор MySQL / SQLite
- ✅ `get_placeholder()` нормализует placeholder для обеих БД
- ✅ `data/repository.py` содержит SQL-запросы и работу с БД (`add_conversion`, `get_all_conversions`, `create_schema`, `add_system_log`)
- ✅ Репозиторий управляет соединениями, коммитами и закрытием `cursor`/`connection`

### 3. Инфраструктура
- ✅ `dependencies.py` инициализирует `connector` и `repo`
- ✅ `start_server.py` запускает `HTTPServer(("0.0.0.0", 8000), MyHTTPHandler)` и корректно закрывает сервер при `KeyboardInterrupt`
- ✅ `logger.py` настроен для записи в файл, поток и базу через `DatabaseHandler`

---

## Что пока не реализовано / не соответствует критериям

### 1. Слой представления
⚠️ `web_server.py` всё ещё содержит бизнес-логику:
- расчёт конверсии выполняется прямо в `do_POST`
- именно здесь происходит вычисление `final_rate` и `result`
- здесь же вызывается сохранение через `repo`

⚠️ `web_server.py` также напрямую делает внешние API-запросы:
- `/get-rates` запрашивает `https://api.frankfurter.dev/v2/rates`
- `/draw_users` запрашивает `https://jsonplaceholder.typicode.com/users`

**Вывод:** слой представления ещё не полностью отделён от бизнес-логики.

### 2. Слой бизнес-логики
❌ `services.py` пока пустой, только заглушка/комментарии
- нет реального модуля для расчёта конверсий
- нет валидации входных данных
- нет обработки внешних API
- нет форматирования результата

### 3. Слой доступа к данным
⚠️ В целом реализован, но:
- транзакционное управление сделано просто через `commit()` на каждую операцию
- можно улучшить обработку ошибок и контекстные менеджеры
- `CurrencyRepository` уже принимает бизнес-данные и хранит их, что правильно

### 4. Инфраструктура
⚠️ `logger.py` настроен, но `start_server.py` его не импортирует, поэтому конфигурация логирования не гарантированно применяется при запуске через `start_server.py`

---

## Степень соответствия требованиям

| Требование | Статус |
|:---|:---|
| `web_server.py` принимает HTTP и отдаёт статику | ✅ Да |
| `web_server.py` не должен содержать бизнес-логику | ⚠️ Частично нет |
| `services.py` выполняет расчёты и валидацию | ❌ Нет |
| `repository.py` содержит всю работу с БД | ✅ Да |
| `db_connector.py` абстрагирует MySQL/SQLite | ✅ Да |
| `start_server.py` запускает `0.0.0.0:8000` | ✅ Да |
| `logger.py` настроен и подключён | ⚠️ Нет, не интегрирован в `start_server.py` |
| Поддержка `DB_TYPE=mysql` и `DB_TYPE=sqlite` | ✅ В теории да |

---

## Рекомендации для следующего шага

1. **Перенести все вычисления конверсии и валидацию** из `web_server.py` в `services.py`
2. **Вынести внешние API-запросы** из `web_server.py` в `services.py`
3. **Сделать `web_server.py` только маршрутизатор** / ответчик / отдачей статики
4. **Подключить `logger.py`** в `start_server.py` или импортировать его при старте

---

## План работ

- [ ] Реализовать функции в `services.py`:
  - `validate_currency_input(from_curr, to_curr, amount)`
  - `get_exchange_rates()` — запрос к Frankfurter API
  - `calculate_conversion(from_curr, to_curr, amount, from_rate, to_rate)` — расчёт
  - `get_user_data()` — запрос к JSONPlaceholder

- [ ] Очистить `web_server.py`:
  - Удалить расчёты из `do_POST`
  - Заменить на вызовы `services.calculate_conversion(...)`
  - Удалить прямые API-запросы, заменить на `services.get_exchange_rates()`

- [ ] Подключить логирование:
  - Импортировать `logger` в `start_server.py`
  - Убедиться, что логи пишутся в БД и файл

- [ ] Тестирование:
  - Проверить работу с `DB_TYPE=mysql`
  - Проверить работу с `DB_TYPE=sqlite`
  - Убедиться, что логи пишутся корректно
