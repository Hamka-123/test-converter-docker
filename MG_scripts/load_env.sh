#!/bin/bash
# load_env.sh

# Определяем корень проекта относительно этого файла
# (так как load_env.sh лежит в MG_scripts, корень — на уровень выше)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${PROJECT_ROOT}/.env" ]; then
    # Экспортируем переменные
    export $(grep -v '^#' "${PROJECT_ROOT}/.env" | xargs)
    # Передаем PROJECT_ROOT дальше, он пригодится для путей
    export PROJECT_ROOT
else
    echo "❌ Ошибка: .env не найден в ${PROJECT_ROOT}"
    exit 1
fi