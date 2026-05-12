# 🏗️ ИНФРАСТРУКТУРА - Распределённая система контейнеров

```mermaid
graph TB
    subgraph Docker["🐳 Docker Environment"]
        direction TB
        
        subgraph network["🌐 Docker Network: currency-net"]
            direction TB
            
            subgraph py_container["Python HTTP Server Container"]
                py["Python 3.14-Alpine<br/>Port: 8000<br/>web_server.py<br/>start_server.py"]
                py_mounts["Bind Mounts:<br/>• /app → ./app<br/>• /http_root"]
            end
            
            subgraph db_container["MariaDB Container"]
                db["MariaDB:latest<br/>Port: 3306<br/>Internal Network<br/>DB: currency_db"]
                db_vol["Volume:<br/>./MariaDB/db_data<br/>:/var/lib/mysql"]
            end
            
            subgraph pma_container["PHPMyAdmin Container"]
                pma["PHPMyAdmin:latest<br/>Port: 80<br/>Exposed: 8081"]
                pma_env["Environment:<br/>PMA_HOST=mariadb-server"]
            end
        end
        
        py -->|connects to| db
        pma -->|connects to| db
    end
    
    client["🖥️ Client<br/>Browser/API"]
    client -->|HTTP:8000| py
    client -->|HTTP:8081| pma
    
    style py_container fill:#4A90E2,color:#fff
    style db_container fill:#F5A623,color:#fff
    style pma_container fill:#7ED321,color:#fff
    style network fill:#E8E8E8,color:#333
    style Docker fill:#F0F0F0,color:#333
```

## 📋 Компоненты инфраструктуры:

| Компонент | Образ | Порт | Функция |
|-----------|--------|------|----------|
| **Python App** | `python:3.14-alpine` | 8000 | HTTP сервер конвертера валют |
| **MariaDB** | `mariadb:latest` | 3306 (сеть) | Хранилище логов и истории конвертаций |
| **PHPMyAdmin** | `phpmyadmin:latest` | 8081 | Веб-интерфейс управления БД |

## 🔗 Сетевая топология:

- **Сеть:** `currency-net` (Docker bridge network)
- Контейнеры видят друг друга по имени хоста
- Изоляция от хоста (кроме пробросанных портов)

## 📦 Управление инфраструктурой (MG_scripts):

```
load_env.sh          → загружает .env переменные
build_app.sh         → docker build Python образа
build_db.sh          → docker build MariaDB + PHPMyAdmin
run_app.sh           → запуск контейнера приложения
run_db.sh            → запуск сети + MariaDB + PHPMyAdmin
```

## 🌍 Переменные окружения (.env):

```
SUBNET=currency-net
DB_HOST=mariadb-server
DB_NAME=currency_db
DB_USER=app_user
DB_PASSWORD=app_password
PY_APP_PORT=8002
PMA_PORT=8081
```

## 📍 Точки подключения:

- **Python API:** `http://localhost:8000`
- **PHPMyAdmin:** `http://localhost:8081`
- **MariaDB CLI:** `localhost:3306` (только внутри сети)
