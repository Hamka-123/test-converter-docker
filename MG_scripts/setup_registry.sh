#!/bin/bash

# Создаем структуру папок, если её нет
mkdir -p auth certs data

# 1. Генерация пароля (пример для демонстрации, в реальном запуске пароль меняют)
echo "[INFO] Generating htpasswd..."
docker run --rm httpd:2.4 htpasswd -Bbn admin temporary_password > auth/htpasswd

# 2. Генерация самоподписанного сертификата
echo "[INFO] Generating TLS certificates..."
openssl req \
    -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key \
    -addext "subjectAltName = DNS:localhost,IP:127.0.0.1" \
    -x509 -days 365 -out certs/domain.crt \
    -subj "/C=IL/ST=Dist/L=Ashdod/O=Corporate/CN=localhost"

# 3. Запуск контейнера
echo "[INFO] Starting Secure Docker Registry..."
docker run -d \
    -p 5001:5000 \
    --restart=always \
    --name secure-corp-registry \
    -v "$(pwd)/data:/var/lib/registry" \
    -v "$(pwd)/auth:/auth" \
    -v "$(pwd)/certs:/certs" \
    -e "REGISTRY_AUTH=htpasswd" \
    -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
    -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
    -e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt" \
    -e "REGISTRY_HTTP_TLS_KEY=/certs/domain.key" \
    registry:2

echo "[SUCCESS] Registry is running on https://localhost:5001"
echo "[IMPORTANT] Don't forget to add certs/domain.crt to your Docker Desktop certs.d folder!"