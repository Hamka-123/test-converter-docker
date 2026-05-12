#!/bin/bash

# 1. Загружаем переменные из .env
source "$(dirname "$0")/load_env.sh"

# 2. Определяем пути
# SCRIPT_DIR — это папка MG_scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# PROJECT_FOLDER — это корень папки с Python сервером
# В твоем дереве папка называется Python_HTTP_server, проверим это:
PROJECT_FOLDER="$(cd "${SCRIPT_DIR}/../Python_HTTP_server" && pwd)"

# 3. Подготовка путей для Docker
# В .env мы договорились использовать префикс PY_ или просто IMAGE_NAME
# Важно: DOCKER_FILE должен указывать на файл внутри PROJECT_FOLDER
FINAL_DOCKERFILE="${PROJECT_FOLDER}/Dockerfile"

# 4. Массив аргументов для Docker
# Используем обновленные переменные из твоего .env:
# PY_IMAGE_NAME и PY_IMAGE_TAG (или IMAGE_NAME и IMAGE_VERSION)
DOCKER_ARGUMENTS=(
    "build"
    "--rm"
    "-f" "${FINAL_DOCKERFILE}"
    "-t" "${PY_IMAGE_NAME}:${PY_IMAGE_TAG}"
    "${PROJECT_FOLDER}"
)

# 5. Вывод команды желтым цветом
printf "\e[33m${DOCKER_ARGUMENTS[*]}\e[0m"

# 6. Запуск Docker
docker "${DOCKER_ARGUMENTS[@]}"