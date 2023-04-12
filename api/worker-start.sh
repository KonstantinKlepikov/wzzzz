#! /usr/bin/env bash
set -e

celery -A app.tasks.worker worker -l info
