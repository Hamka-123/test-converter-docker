# Используем официальный образ как фундамент
FROM mariadb:latest

# (Опционально) Если хочешь, чтобы при запуске сразу создавалась таблица,
# можно положить .sql файл в папку /docker-entrypoint-initdb.d/
# COPY ./init.sql /docker-entrypoint-initdb.d/

# Оставляем стандартный порт
EXPOSE 3306