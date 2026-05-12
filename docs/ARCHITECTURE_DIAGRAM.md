# 🏛️ АРХИТЕКТУРА - Многослойная система приложения

```mermaid
graph TB
    subgraph presentation["🎨 Слой Представления (Web Server)"]
        direction TB
        ws["web_server.py<br/>BaseHTTPRequestHandler<br/>- HTTP запросы GET/POST<br/>- Маршрутизация по путям<br/>- JSON парсинг/отправка<br/>- Раздача static файлов"]
    end
    
    subgraph business["💼 Слой Бизнес-Логики (Services)"]
        direction TB
        svc["services.py<br/>- Расчёты конвертации<br/>- Валидация данных<br/>- Внешние API (requests)<br/>- Форматирование результатов"]
    end
    
    subgraph data_access["💾 Слой Доступа к Данным"]
        direction TB
        connector["db_connector.py<br/>- MySQL/SQLite адаптер<br/>- Управление подключением<br/>- Нормализация placeholder"]
        repo["repository.py<br/>- add_conversion()<br/>- create_schema()<br/>- SQL запросы"]
    end
    
    subgraph infrastructure["🔧 Инфраструктура & Зависимости"]
        direction TB
        deps["dependencies.py<br/>- Инициализация объектов<br/>- Внедрение зависимостей<br/>- Singleton паттерн"]
        entry["start_server.py<br/>- HTTPServer(0.0.0.0:8000)<br/>- serve_forever()<br/>- Graceful shutdown"]
    end
    
    subgraph database["🗄️ Базы Данных"]
        direction TB
        mysql["MySQL/MariaDB<br/>Таблицы:<br/>• conversions<br/>• logs"]
        sqlite["SQLite<br/>logs.db<br/>(fallback)"]
    end
    
    subgraph static["📄 Статические ресурсы"]
        direction TB
        web["static/<br/>- index.html<br/>- style.css<br/>- script.js"]
    end
    
    client["👤 Client<br/>Browser/API"]
    
    client -->|HTTP Request| ws
    ws -->|calls| svc
    ws -->|serves| static
    svc -->|calls| repo
    repo -->|uses| connector
    connector -->|DB_TYPE=mysql| mysql
    connector -->|DB_TYPE=sqlite| sqlite
    
    deps -->|initializes| connector
    deps -->|initializes| repo
    entry -->|imports| deps
    entry -->|runs| ws
    
    ws -->|response| client
    
    style presentation fill:#4A90E2,color:#fff,stroke:#2E5C8A,stroke-width:3px
    style business fill:#F5A623,color:#fff,stroke:#C17A1A,stroke-width:3px
    style data_access fill:#7ED321,color:#fff,stroke:#5AA917,stroke-width:3px
    style infrastructure fill:#9B9B9B,color:#fff,stroke:#666,stroke-width:3px
    style database fill:#E94B3C,color:#fff,stroke:#B83A2E,stroke-width:3px
    style static fill:#6C63FF,color:#fff,stroke:#4A3FB8,stroke-width:3px
```

## 📐 Архитектурный паттерн: **Многослойная архитектура (Layered Architecture)**

### Слои приложения:

#### 1️⃣ **Слой Представления** (Presentation Layer)
- **Файл:** `web_server.py`
- **Ответственность:**
  - Приём HTTP запросов
  - Парсинг JSON-тела запроса
  - Маршрутизация (определение какой endpoint вызвать)
  - Отправка JSON ответов
  - Раздача статических файлов (HTML/CSS/JS)
- **Ограничение:** Не содержит бизнес-логику, не знает о БД

#### 2️⃣ **Слой Бизнес-Логики** (Business Logic Layer)
- **Файл:** `services.py`
- **Ответственность:**
  - Расчёты конвертации валют
  - Валидация входных параметров
  - Работа с внешними API (requests)
  - Форматирование данных (isoformat, рounding)
- **Ограничение:** Не знает о HTTP, работает только с Python объектами

#### 3️⃣ **Слой Доступа к Данным** (Data Access Layer)
- **Файлы:** `data/db_connector.py`, `data/repository.py`
- **Ответственность:**
  - Абстракция подключения к БД (MySQL или SQLite)
  - SQL запросы (INSERT, SELECT)
  - Сохранение истории и логов
  - Управление транзакциями
- **Ограничение:** Не принимает решений, только исполняет команды

#### 4️⃣ **Инфраструктура** (Infrastructure)
- **Файлы:** `dependencies.py`, `start_server.py`, `logger.py`
- **Ответственность:**
  - Инициализация объектов (DBConnector, Repository)
  - Конфигурация логирования
  - Запуск HTTP сервера
  - Управление жизненным циклом приложения

---

## 🔄 Поток данных (Data Flow):

```
Client HTTP Request
    ↓
web_server.py (парсинг, маршрутизация)
    ↓
services.py (бизнес-логика, расчёты)
    ↓
repository.py (подготовка SQL)
    ↓
db_connector.py (выбор БД, адаптация)
    ↓
MySQL/MariaDB или SQLite (сохранение)
    ↓
(обратный путь)
web_server.py (JSON ответ)
    ↓
Client
```

---

## ✅ Преимущества этой архитектуры:

| Сценарий | Решение |
|----------|---------|
| **Смена БД** (MySQL → PostgreSQL) | Переписать только `db_connector.py` |
| **Новый интерфейс** (Telegram бот) | Создать новый handler, вызвать `services.py` |
| **Баг в расчётах** | Исправить в одном месте — `services.py` |
| **Изменение дизайна** | Редактировать `static/` |
| **Добавить кэширование** | Добавить слой между `web_server` и `services` |
| **Написать тесты** | Тестировать каждый слой независимо |

---

## 🚀 Итог:

Это **распределённая монолитная архитектура** с чётким разделением ответственности:
- ✅ Легко тестировать каждый слой отдельно
- ✅ Легко добавлять новые возможности
- ✅ Легко менять реализацию (БД, фреймворк, интерфейс)
- ✅ Легко нанимать новых разработчиков (структура понятна)
- ⚠️ Может стать узким местом при масштабировании (используй микросервисы)

**Следующий шаг:** Разделить на микросервисы, если система станет слишком большой.
