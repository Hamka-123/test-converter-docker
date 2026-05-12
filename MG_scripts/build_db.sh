#!/bin/bash
# Подключаем загрузчик переменных
source "$(dirname "$0")/load_env.sh"

printf "\e[33m--- СБОРКА ОБРАЗОВ БАЗЫ ДАННЫХ ---\e[0m"

# Сборка MariaDB
# Мы указываем путь к папке MariaDB, где лежит твой Dockerfile
docker build -t "${DB_IMAGE_NAME}:${DB_IMAGE_TAG}" "${PROJECT_ROOT}/MariaDB"

# Сборка PHPMyAdmin
docker build -t "${PMA_IMAGE_NAME}:${PMA_IMAGE_TAG}" "${PROJECT_ROOT}/PHP_My_Admin"

printf "\e[32m✅ Образы успешно собраны и готовы к работе!\e[0m"