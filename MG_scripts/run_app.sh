#!/bin/bash

# 1. Загружаем переменные из .env
source "$(dirname "$0")/load_env.sh"

# 2. Определяем пути
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Убедись, что папка называется именно Python_HTTP_server, как в твоем tree
PROJECT_FOLDER="$(cd "${SCRIPT_DIR}/../Python_HTTP_server" && pwd)"

PY_CONTAINER_NAME="python_server_container_${PMA_IMAGE_TAG}"

# 3. Массив аргументов
# ВНИМАНИЕ: Каждая часть флага (ключ и значение) должна быть отдельным элементом массива!
DOCKER_ARGUMENTS=(
    "run"
    "--detach"
    "--interactive"
    "--tty"
    "--rm"
    "--name" "${PY_CONTAINER_NAME:-python_app_default}" # Если пусто, даст имя по умолчанию
    "--network" "${SUBNET}"
    "--publish" "${PY_APP_PORT}:8000"
    "--mount" "type=bind,source=${PROJECT_FOLDER}/app,target=/app"
    "--mount" "type=bind,source=${PROJECT_FOLDER}/http_root,target=/http_root"
    "-e" "DB_TYPE=${DB_TYPE}"
    "${PY_IMAGE_NAME}:${PY_IMAGE_TAG}"
)

# 4. Вывод команды желтым цветом (для отладки)
printf "\e[33m${DOCKER_ARGUMENTS[*]}\e[0m"

# 5. Запуск Docker с логированием
# Мы используем "${DOCKER_ARGUMENTS[@]}" в кавычках, чтобы пробелы в путях не ломали команду
# docker "${DOCKER_ARGUMENTS[@]}" >> "${SCRIPT_DIR}/container.log" 2>&1
docker "${DOCKER_ARGUMENTS[@]}" 