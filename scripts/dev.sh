#! /usr/bin/env sh

# Exit in case of error
set -e

INSTALL_DEV=true \
docker compose \
-f docker-compose.yml \
-f docker-compose.dev.yml \
config > docker-stack.yml

docker compose -f docker-stack.yml build
docker compose -f docker-stack.yml down --remove-orphans
docker compose -f docker-stack.yml up -d
