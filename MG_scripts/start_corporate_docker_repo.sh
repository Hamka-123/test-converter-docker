#!/bin/bash 

# --- Unsecure ---

# docker run -d \
#     -p 5001:5000 \
#     --restart=always \
#     --name corporate-local-repo \
#     -v $HOME/docker_mirror_data:/var/lib/registry \
#     registry:2

# http://localhost:5001/v2/_catalog
# http://localhost:5001/v2/python_http_server/tags/list

# --- Secure ---

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

# docker tag python_http_server:1.0.0 localhost:5001/python_http_server:1.0.0

# docker push localhost:5001/python_http_server:1.0.0

# https://localhost:5001/v2/_catalog
