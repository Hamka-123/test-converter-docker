#!/bin/bash

# 1. Загружаем статические переменные из .env
# Мы используем экспорт, чтобы переменные были доступны командам docker
source "$(dirname "$0")/load_env.sh"

# 2. ДИНАМИЧЕСКИЕ ПЕРЕМЕННЫЕ (Склеиваем то, что нельзя в .env)
# Собираем полные имена образов (чертежей)
DB_FULL_IMAGE="${DB_IMAGE_NAME}:${DB_IMAGE_TAG}"
PMA_FULL_IMAGE="${PMA_IMAGE_NAME}:${PMA_IMAGE_TAG}"

# Собираем имена контейнеров (экземпляров)
# ВАЖНО: Мы используем DB_HOST для имени контейнера базы, 
# чтобы PHPMyAdmin мог найти его по этому же имени в сети.
DB_ACTUAL_NAME="${DB_HOST}" 
PMA_ACTUAL_NAME="phpmyadmin-gui_${PMA_IMAGE_TAG}"

# Формируем путь к данным (Volume)
# Используем $(pwd), чтобы путь всегда был актуальным для твоего Мака
DB_VOLUME_BIND="$(pwd)/../MariaDB/db_data:/var/lib/mysql"

# --- ЛОГИКА ЗАПУСКА ---

# 3. Создаем сеть, если её еще нет
docker network create $SUBNET 2>/dev/null || true

# 4. Запускаем MariaDB
# Мы используем кавычки для путей, на случай если в именах папок есть пробелы
docker run -d \
--name "$DB_ACTUAL_NAME" \
--network "$SUBNET" \
-e MARIADB_DATABASE="$DB_NAME" \
-e MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD} \
-e MYSQL_USER=${DB_USER} \
-e MYSQL_PASSWORD=${DB_PASSWORD} \
-v "$DB_VOLUME_BIND" \
"$DB_FULL_IMAGE"

# 5. Запускаем PHPMyAdmin
docker run -d \
--name "$PMA_ACTUAL_NAME" \
--network "$SUBNET" \
-e PMA_HOST="$DB_ACTUAL_NAME" \
-p "$PMA_PORT:80" \
"$PMA_FULL_IMAGE"

echo "✅ Инфраструктура запущена!"
echo "Database host: $DB_ACTUAL_NAME"
echo "PHPMyAdmin: http://localhost:$PMA_PORT"